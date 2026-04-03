# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, FreelanceProfile, ClientProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'freelance':
            FreelanceProfile.objects.create(user=instance)
        elif instance.role == 'client':
            ClientProfile.objects.create(user=instance)

