# chat/models.py
from django.db import models

from missions.models import Mission
from users.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="chat_files/", null=True, blank=True)  # 🔥 AJOUT
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.email} → {self.content or 'Fichier'}"

