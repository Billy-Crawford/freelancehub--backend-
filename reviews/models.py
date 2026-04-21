# reviews/models.py
from django.db import models
from django.conf import settings
from missions.models import Mission

User = settings.AUTH_USER_MODEL

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_given")
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_received")
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)

    rating = models.IntegerField()  # 1 à 5
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reviewer", "mission")  # 1 avis par mission

    def __str__(self):
        return f"{self.reviewer} → {self.reviewed} ({self.rating})"

