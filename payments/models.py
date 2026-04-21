# payments/models.py
from django.db import models
from users.models import User
from missions.models import Mission

class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("held", "Held"),
        ("released", "Released"),
        ("refunded", "Refunded"),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_sent")
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_received")
    mission = models.OneToOneField(Mission, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} → {self.freelancer} ({self.amount})"

