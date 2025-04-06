from src.objets.models import DemandeSuppressionObjet
from django.urls import reverse
from .models import Apparence


def admin_notifications(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # Récupérer les demandes en attente
        demandes = DemandeSuppressionObjet.objects.filter(status='en attente')
        # On construit une liste de notifications
        notifications = []
        for d in demandes:
            notifications.append({
                'title': f"Demande de suppression: {d.objet.nom}",
                'link': reverse('traiter_demande_suppression', args=[d.id])  # par ex. page d'admin pour accepter/refuser
            })
        return {'admin_notifications': notifications}
    return {}

def site_settings(request):
    # On récupère l'instance d'Apparence, en créant une nouvelle si nécessaire (id=1)
    apparence, created = Apparence.objects.get_or_create(id=1)
    return {'apparence': apparence}

