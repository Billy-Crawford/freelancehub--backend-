from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Review
from .serializers import ReviewSerializer
from missions.models import Mission


class CreateReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, mission_id):
        mission = get_object_or_404(Mission, id=mission_id)

        # ❌ mission pas terminée
        if mission.status != "completed":
            raise ValidationError("La mission n'est pas terminée")

        user = request.user

        # 🔹 déterminer qui est noté
        if user == mission.client:
            # client note freelance
            app = mission.applications.filter(status="accepted").first()
            if not app:
                raise ValidationError("Aucun freelance trouvé")

            reviewed = app.freelancer

        else:
            # freelance note client
            reviewed = mission.client

        # ❌ double review
        if Review.objects.filter(reviewer=user, mission=mission).exists():
            raise ValidationError("Vous avez déjà noté cette mission")

        review = Review.objects.create(
            reviewer=user,
            reviewed=reviewed,
            mission=mission,
            rating=request.data.get("rating"),
            comment=request.data.get("comment", "")
        )

        return Response(ReviewSerializer(review).data)


class UserReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return Review.objects.filter(reviewed_id=user_id).order_by("-created_at")