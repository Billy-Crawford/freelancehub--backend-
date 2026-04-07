from django.db import models
from django.conf import settings
from missions.models import Mission

User = settings.AUTH_USER_MODEL

class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
    ]

    mission = models.OneToOneField(Mission, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_sent")
    freelance = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_received")

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} → {self.freelance} ({self.amount})"

