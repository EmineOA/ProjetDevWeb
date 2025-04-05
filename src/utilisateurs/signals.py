from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.conf import settings

@receiver(user_logged_in)
def add_xp_on_login(sender, request, user, **kwargs):
    # Exemple : ajouter 10 XP à chaque connexion
    user.xp += 10
    user.save(update_fields=['xp'])
    # Mettre à jour le rôle si les seuils sont atteints
    user.update_role()
