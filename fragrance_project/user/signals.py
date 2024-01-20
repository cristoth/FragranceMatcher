from django.db.models.signals import post_save  # signal fired after an object is saved
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)  # post_save is the signal (when user is created)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)  # post_save is the signal (when user is saved)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
