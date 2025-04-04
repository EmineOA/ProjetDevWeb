from django.shortcuts import render, get_object_or_404, redirect
from src.utilisateurs.models import Utilisateur
from src.objets.models import ObjetConnecte, Rapport
from .forms import UserAddForm, UserUpdateForm

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

def gestion_utilisateurs(request):
    """Vue pour lister tous les utilisateurs et gérer l'accès au formulaire d'ajout."""
    utilisateurs = Utilisateur.objects.all()
    context = {'utilisateurs': utilisateurs}
    return render(request, 'gestion_utilisateurs.html', context)

def user_add(request):
    """Vue pour ajouter un nouvel utilisateur."""
    if request.method == 'POST':
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionnel: définir un mot de passe par défaut
            user.set_password('mdpParDefaut123')
            user.save()
            return redirect('gestion_utilisateurs')
    else:
        form = UserAddForm()
    return render(request, 'user_add.html', {'form': form})

def user_edit(request, user_id):
    """Vue pour modifier un utilisateur existant."""
    user = get_object_or_404(Utilisateur, id=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('gestion_utilisateurs')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'user_edit.html', {'form': form, 'user': user})

def user_delete(request, user_id):
    """Vue pour supprimer un utilisateur."""
    user = get_object_or_404(Utilisateur, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('gestion_utilisateurs')
    return render(request, 'user_delete_confirm.html', {'user': user})

