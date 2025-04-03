from django.db import models
from src.utilisateurs.models import Utilisateur

class CategorieObjet(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Salle(models.Model):
    nom = models.CharField(max_length=100)
    localisation = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nom

class ObjetConnecte(models.Model):
    ETATS = (
        ('activé', 'Activé'),
        ('en veille', 'En veille'),
        ('hors ligne', 'Hors ligne'),
    )
    nom = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    # Utilisation d'une clé étrangère pour permettre la gestion des catégories via le module Administration
    categorie = models.ForeignKey(CategorieObjet, on_delete=models.SET_NULL, null=True, blank=True, related_name='objets')
    etat = models.CharField(max_length=20, choices=ETATS, default='hors ligne')
    # Association à une salle pour la gestion des pièces/locaux
    salle = models.ForeignKey(Salle, null=True, blank=True, on_delete=models.SET_NULL, related_name='objets')
    consommation_energetique = models.FloatField(null=True, blank=True)
    connectivite = models.CharField(max_length=50, null=True, blank=True)
    derniere_interaction = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='objets/', null=True, blank=True)

    def __str__(self):
        return self.nom

class DemandeSuppressionObjet(models.Model):
    STATUTS = (
        ('en attente', 'En attente'),
        ('acceptée', 'Acceptée'),
        ('refusée', 'Refusée'),
    )
    objet = models.ForeignKey(ObjetConnecte, on_delete=models.CASCADE, related_name='demandes')
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='demandes_suppression')
    raison = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUTS, default='en attente')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_traitement = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Demande pour {self.objet.nom} par {self.utilisateur.username}"

class ServiceConfiguration(models.Model):
    """
    Permet de configurer des paramètres spécifiques pour un objet connecté,
    par exemple : température cible pour un radiateur, heure de fonctionnement pour des LEDs, etc.
    Les paramètres sont stockés sous forme de JSON pour une flexibilité maximale.
    """
    objet = models.OneToOneField(ObjetConnecte, on_delete=models.CASCADE, related_name='configuration')
    parametres = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Configuration de {self.objet.nom}"

# Optionnel : Modèle pour générer et stocker des rapports avancés (export CSV/PDF, statistiques, etc.)
class Rapport(models.Model):
    titre = models.CharField(max_length=100)
    contenu = models.TextField()  # Ce contenu peut être le résultat d'une analyse ou un chemin vers un fichier exporté
    date_creation = models.DateTimeField(auto_now_add=True)
    type_rapport = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.titre

# Optionnel : Modèle pour stocker des paramètres généraux de la plateforme, modifiables par l'administrateur
class ConfigurationGlobale(models.Model):
    cle = models.CharField(max_length=100, unique=True)
    valeur = models.TextField()

    def __str__(self):
        return self.cle
