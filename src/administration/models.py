from django.db import models

class Apparence(models.Model):
    # Code couleur en hexadécimal pour le background du site (exemple : #ffffff)
    background_color = models.CharField(
        max_length=7,
        default='#ffffff',
        help_text="Code couleur en hexadécimal pour le background (ex: #ffffff)"
    )
    # Logo du site, stocké via un ImageField (assure-toi d'avoir Pillow installé)
    logo = models.ImageField(
        upload_to='logos/',
        blank=True,
        null=True,
        help_text="Logo du site"
    )

    def __str__(self):
        return "Apparence de la plateforme"

class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    # Un lien optionnel vers la page liée à la notification
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title