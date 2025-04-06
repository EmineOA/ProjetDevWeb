from src.objets.models import DemandeSuppressionObjet
from django.urls import reverse


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
