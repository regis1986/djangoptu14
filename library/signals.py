from django.db.models.signals import post_save # signalas
from django.contrib.auth.models import User # siuntejas
from django.dispatch import receiver # gavejas (dekoratorius)
from .models import Profilis

@receiver(post_save, sender=User)
def create_profile(sender,
                   instance, # sukurtas USer klases objektas
                   created,  # boolean, kai USer obj sukuriamas, jis True
                   **kwargs
                   ):
    if created:
        Profilis.objects.create(user=instance)
        # print('kwargs': , kwargs)
