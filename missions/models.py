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