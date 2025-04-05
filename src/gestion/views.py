from django.shortcuts import render, redirect
from django.contrib import messages
from src.utilisateurs.decorators import role_required

@role_required('gestion')
def gestion_home(request):
    """
    Page d’accueil du module Gestion.
    """
    return render(request, 'gestion/home.html')

@role_required('gestion')
def gestion_objets(request):
    """
    Page pour gérer les objets connectés (ajout, modification, suppression).
    """
    return render(request, 'gestion/objets.html')

@role_required('gestion')
def export_data(request):
    """
    Page (ou action) pour exporter des données en CSV/PDF.
    """
    return render(request, 'gestion/export.html')
