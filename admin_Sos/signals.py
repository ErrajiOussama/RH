from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from django.contrib.auth.models import User,Group

@receiver(post_save, sender=User)
def create_profil(sender,instance,created, **kwargs):
    if created:
        Collaborateur.objects.create(
            user=instance,
            )
        print('Profile created')
"""
@receiver(post_save, sender=User)
def update_profil(sender,instance,created, **kwargs):
    if created == False:
        instance.Client.save()
        print('Profile updated')
"""

post_save.connect(create_profil,sender=User)