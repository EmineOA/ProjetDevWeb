from django.db import models

class Apparence(models.Model):
    # Stocke le code couleur du thème (en hexadécimal)
    theme_color = models.CharField(max_length=7, default='#ffffff', help_text="Code couleur en hexadécimal (ex: #ffffff)")
    # URL du logo
    logo_url = models.URLField(blank=True, null=True, help_text="URL de l'image du logo")

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