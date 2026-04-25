# missions/models.py
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Mission(models.Model):
    STATUS_CHOICES = (
        ('open', 'Ouverte'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminée'),
        ('cancelled', 'Annulée'),
    )


    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='missions')

    title = models.CharField(max_length=255)
    description = models.TextField()

    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()

    skills_required = models.JSONField(default=list)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MissionApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="applications")
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True)  # optionnel
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("mission", "freelancer")  # un freelance ne peut postuler qu'une fois par mission

    def __str__(self):
        return f"{self.freelancer.email} → {self.mission.title} [{self.status}]"

