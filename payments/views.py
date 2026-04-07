from rest_framework import generics, permissions
from .models import Payment
from .serializers import PaymentSerializer
from missions.models import Mission
from django.shortcuts import get_object_or_404

class CreatePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        mission_id = self.kwargs.get("mission_id")
        mission = get_object_or_404(Mission, id=mission_id)

        if self.request.user != mission.client:
            raise PermissionError("Seul le client peut payer")

        application = mission.applications.filter(status="accepted").first()

        serializer.save(
            mission=mission,
            client=self.request.user,
            freelance=application.freelancer,
            amount=mission.budget,
            status="completed"
        )

