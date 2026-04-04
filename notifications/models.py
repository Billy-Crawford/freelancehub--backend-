# notifications/models.py
from django.db import models
from users.models import User

class Notification(models.Model):
    NOTIF_TYPES = [
        ("new_mission", "Nouvelle mission"),
        ("application_status", "Statut candidature"),
        ("payment", "Paiement"),
        ("message", "Message"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=20, choices=NOTIF_TYPES)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} → {self.user.email}"

