# missions/views.py
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.http import FileResponse

from .models import Mission, MissionApplication
from .serializers import MissionSerializer, MissionApplicationSerializer
from .permissions import IsClient, IsOwnerOrReadOnly

from notifications.models import Notification
from utils.pdf_utils import generate_mission_pdf

# 🔹 Liste + création des missions
class MissionListCreateView(generics.ListCreateAPIView):
    queryset = Mission.objects.all().order_by('-created_at')
    serializer_class = MissionSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsClient()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        mission = serializer.save(client=self.request.user)

        # 🔹 Notifier tous les freelances
        from users.models import User
        for freelance in User.objects.filter(role="freelance"):
            Notification.objects.create(
                user=freelance,
                type="new_mission",
                content=f"Nouvelle mission disponible : {mission.title}"
            )


# 🔹 Détail + update + delete
class MissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# 🔹 Postuler à une mission
class ApplyMissionView(generics.CreateAPIView):
    serializer_class = MissionApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        mission_id = self.kwargs.get("mission_id")
        mission = get_object_or_404(Mission, id=mission_id)

        # Vérifier si l'utilisateur est freelance via son profil
        if not hasattr(self.request.user, 'freelance_profile'):
            raise ValidationError("Seuls les freelances peuvent postuler.")

        # Vérifier candidature existante
        if MissionApplication.objects.filter(mission=mission, freelancer=self.request.user).exists():
            raise ValidationError("Vous avez déjà postulé à cette mission.")

        application = serializer.save(mission=mission, freelancer=self.request.user)

        # 🔹 Notifier le client que quelqu’un a postulé
        Notification.objects.create(
            user=mission.client,
            type="application_status",
            content=f"{self.request.user.email} a postulé à votre mission '{mission.title}'."
        )


# 🔹 Mettre à jour le statut d'une candidature
class UpdateApplicationStatusView(generics.UpdateAPIView):
    serializer_class = MissionApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Le client ne peut gérer que ses missions
        return MissionApplication.objects.filter(mission__client=self.request.user)

    def perform_update(self, serializer):
        status = self.request.data.get("status")
        if status not in ["accepted", "rejected"]:
            raise ValidationError("Status invalide.")

        application = serializer.save(status=status)

        # 🔹 Notifier le freelance de l'acceptation ou du refus
        Notification.objects.create(
            user=application.freelancer,
            type="application_status",
            content=f"Votre candidature pour '{application.mission.title}' a été {application.status}."
        )


# 🔹 Génération du PDF pour une mission
# ⚠️ Cette view n’est pas DRF, c’est une view Django classique
def mission_pdf_view(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    pdf_buffer = generate_mission_pdf(mission)
    return FileResponse(pdf_buffer, as_attachment=True, filename=f"{mission.title}.pdf")

