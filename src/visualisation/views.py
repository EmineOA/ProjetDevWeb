from django.contrib.auth.decorators import login_required
from django.db.models import Q

from src.utilisateurs.decorators import role_required
from src.objets.models import ObjetConnecte
from django.shortcuts import get_object_or_404
from src.utilisateurs.models import Utilisateur
from .forms import EditProfilForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, update_session_auth_hash

User = get_user_model()

@role_required('visualisation')
def visualisation_home(request):
    """
    Affiche la page d’accueil du module Visualisation avec une liste d’objets connectés.
    La barre de recherche avec filtres (état et catégorie) est disponible dans le template.
    """
    objets = ObjetConnecte.objects.all()
    # Si vous avez un modèle pour les catégories, récupérez-les, sinon passez une liste vide
    categories = []  # Par exemple : CategorieObjet.objects.all()
    context = {
        'objets': objets,
        'categories': categories,
    }
    return render(request, 'visualisation/home.html', context)

@role_required('visualisation')
def visualisation_profil(request):
    # Pour la section "Mon Profil" et la liste des autres profils
    utilisateurs = Utilisateur.objects.exclude(id=request.user.id)
    return render(request, 'visualisation/profil.html', {'utilisateurs': utilisateurs})

@role_required('visualisation')
def visualisation_objets(request):
    # Ici, vous récupérez la liste des objets connectés
    from src.objets.models import ObjetConnecte
    objets = ObjetConnecte.objects.all()
    return render(request, 'visualisation/objets.html', {'objets': objets})


def objet_detail(request, objet_id):
    """
    Affiche le détail d’un objet connecté.
    """
    objet = get_object_or_404(ObjetConnecte, id=objet_id)
    context = {'objet': objet}
    return render(request, 'visualisation/objet_detail.html', context)

def profil(request):
    """
    Affiche le profil de l’utilisateur connecté.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'visualisation/profil.html', {'user': request.user})


def modifier_profil(request):
    """
    Permet à l’utilisateur de modifier son profil.
    (Ici, vous devrez probablement utiliser un formulaire pour la modification.)
    """
    if not request.user.is_authenticated:
        return redirect('login')

    # Supposons que vous ayez un formulaire 'ProfilForm'
    # from .forms import ProfilForm
    # if request.method == 'POST':
    #     form = ProfilForm(request.POST, request.FILES, instance=request.user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('profil')
    # else:
    #     form = ProfilForm(instance=request.user)
    #
    # context = {'form': form}

    # Pour l'instant, nous renvoyons simplement une page de modification (à compléter)
    return render(request, 'visualisation/modifier_profil.html', {'user': request.user})

def visualisation_recherche_objet(request):
    query = request.GET.get('q', '')
    etat = request.GET.get('etat', '')
    categorie = request.GET.get('categorie', '')

    objets = ObjetConnecte.objects.all()
    if query:
        objets = objets.filter(nom__icontains=query)
    if etat:
        objets = objets.filter(etat=etat)
    if categorie:
        objets = objets.filter(categorie_id=categorie)

    context = {
        'objets': objets,
        'query': query,
        'etat': etat,
        'categorie': categorie,
    }
    return render(request, 'visualisation/search_objet.html', context)


def visualisation_recherche_objet(request):
    query = request.GET.get('q', '')
    etat = request.GET.get('etat', '')
    categorie = request.GET.get('categorie', '')

    objets = ObjetConnecte.objects.all()
    if query:
        objets = objets.filter(nom__icontains=query)
    if etat:
        objets = objets.filter(etat=etat)
    if categorie:
        objets = objets.filter(categorie_id=categorie)

    context = {
        'objets': objets,
        'query': query,
        'etat': etat,
        'categorie': categorie,
    }
    return render(request, 'visualisation/search_objet.html', context)

def edit_profil(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfilForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('visualisation_profil')
    else:
        form = EditProfilForm(instance=user)
    return render(request, 'visualisation/edit_profil.html', {'form': form})

def view_profil(request, user_id=None):
    """
    Affiche le profil d'un utilisateur.
    Si user_id est None, affiche le profil de l'utilisateur connecté.
    Sinon, affiche le profil de l'utilisateur correspondant à user_id.
    """
    if user_id is None:
        user_profile = request.user
    else:
        user_profile = get_object_or_404(Utilisateur, id=user_id)
    return render(request, 'visualisation/view_profil.html', {'user_profile': user_profile})


@login_required
def view_profiles(request):
    """
    Affiche la liste des profils (pour consulter les autres membres).
    Permet une recherche par username, prénom ou nom et un filtre par type de membre.
    """
    query = request.GET.get('q', '')
    type_membre = request.GET.get('type_membre', '')
    profiles = Utilisateur.objects.all()

    if query:
        profiles = profiles.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    if type_membre:
        profiles = profiles.filter(type_membre=type_membre)

    context = {
        'profiles': profiles,
        'query': query,
        'type_membre': type_membre,
    }
    return render(request, 'visualisation/view_profiles.html', context)

def search_profiles(request):
    query = request.GET.get('q', '')
    type_membre = request.GET.get('type_membre', '')
    genre = request.GET.get('genre', '')

    # Commencez avec tous les utilisateurs
    results = Utilisateur.objects.all()
    if query:
        results = results.filter(username__icontains=query)
    if type_membre:
        results = results.filter(type_membre=type_membre)
    if genre:
        results = results.filter(sexe=genre)

    context = {
        'search_results': results,
    }
    return render(request, 'visualisation/view_profiles.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not request.user.check_password(old_password):
            messages.error(request, "L'ancien mot de passe est incorrect.")
        elif new_password1 != new_password2:
            messages.error(request, "Les nouveaux mots de passe ne correspondent pas.")
        elif not new_password1:
            messages.error(request, "Le nouveau mot de passe ne peut être vide.")
        else:
            request.user.set_password(new_password1)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Pour ne pas déconnecter l'utilisateur
            messages.success(request, "Votre mot de passe a été mis à jour avec succès.")
            return redirect('visualisation_profil')  # Redirigez vers la page du profil

    return render(request, 'visualisation/change_password.html')


