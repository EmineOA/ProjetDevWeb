from django.shortcuts import render, redirect
from django.contrib import messages
from src.utilisateurs.decorators import role_required

@role_required('visualisation')
def visualisation_home(request):
    """
    Page d’accueil du module Visualisation.
    """
    return render(request, 'visualisation/home.html')

@role_required('visualisation')
def visualisation_profil(request):
    """
    Page pour gérer le profil (ou afficher le profil) dans le module Visualisation.
    """
    return render(request, 'visualisation/profil.html')

@role_required('visualisation')
def visualisation_objets(request):
    """
    Page pour consulter les objets connectés (vue 'read-only' pour un utilisateur simple).
    """
    return render(request, 'visualisation/objets_connectes.html')
