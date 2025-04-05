from django.db import models

class Apparence(models.Model):
    # Stocke le code couleur du thème (en hexadécimal)
    theme_color = models.CharField(max_length=7, default='#ffffff', help_text="Code couleur en hexadécimal (ex: #ffffff)")
    # URL du logo
    logo_url = models.URLField(blank=True, null=True, help_text="URL de l'image du logo")

    def __str__(self):
        return "Apparence de la plateforme"