from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ('simple', 'Simple'),
    ('complexe', 'Complexe'),
    ('administrateur', 'Administrateur'),
)

class Utilisateur(AbstractUser):
    pseudo = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True, blank=True)
    sexe = models.CharField(max_length=20, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    type_membre = models.CharField(max_length=50, choices=ROLE_CHOICES, default='simple')
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    xp = models.PositiveIntegerField(default=0)
    niveau = models.CharField(max_length=20, default='Débutant')
    est_verifie = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    derniere_connexion = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Si l'utilisateur est superuser, on force le rôle à 'administrateur'
        if self.is_superuser:
            self.type_membre = 'administrateur'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class ActionUtilisateur(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='actions')
    type_action = models.CharField(max_length=50)
    points_gagnes = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    date_action = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.type_action}"
