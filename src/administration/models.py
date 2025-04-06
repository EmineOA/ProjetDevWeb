from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

class Apparence(models.Model):
    # URL du logo du site
    logo = models.URLField(blank=True, null=True, help_text="URL de l'image du logo")
    # Code couleur hexadécimal pour le background
    background_color = models.CharField(
        max_length=7,
        default='#ffffff',
        help_text="Code couleur en hexadécimal (ex: #ffffff)"
    )

    def __str__(self):
        return "Apparence de la plateforme"

@receiver(pre_save, sender=User)
def assign_admin_role(sender, instance, **kwargs):
    if instance.is_superuser:
        instance.type_membre = 'administrateur'

class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    # Un lien optionnel vers la page liée à la notification
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title