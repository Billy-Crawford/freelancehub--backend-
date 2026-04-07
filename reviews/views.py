from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer
from missions.models import Mission
from django.shortcuts import get_object_or_404

class CreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        mission_id = self.kwargs.get("mission_id")
        mission = get_object_or_404(Mission, id=mission_id)

        user = self.request.user

        # déterminer qui est évalué
        if user == mission.client:
            reviewed = mission.applications.filter(status="accepted").first().freelancer
        else:
            reviewed = mission.client

        serializer.save(
            reviewer=user,
            reviewed=reviewed,
            mission=mission
        )

        