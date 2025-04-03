from django.shortcuts import render
from src.utilisateurs.models import Utilisateur
from src.objets.models import ObjetConnecte, Rapport

def tableau_de_bord(request):
    context = {}
    return render(request, 'tableau_de_bord.html', context)

def gestion_utilisateurs(request):
    utilisateurs = Utilisateur.objects.all()
    context = {'utilisateurs': utilisateurs}
    return render(request, 'gestion_utilisateurs.html', context)

def gestion_objets_avances(request):
    objets = ObjetConnecte.objects.all()
    context = {'objets': objets}
    return render(request, 'gestion_objets_avances.html', context)

def securite_maintenance(request):
    # Ici tu implémenteras la logique pour la mise à jour des mots de passe, sauvegardes, etc.
    context = {}
    return render(request, 'securite_maintenance.html', context)

def personnalisation(request):
    # Logique pour modifier l'apparence ou d'autres paramètres
    context = {}
    return render(request, 'personnalisation.html', context)

def rapports_avances(request):
    rapports = Rapport.objects.all()
    context = {'rapports': rapports}
    return render(request, 'rapports_avances.html', context)
