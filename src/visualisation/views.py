from django.contrib.auth.decorators import login_required
from django.db.models import Q

from src.utilisateurs.decorators import role_required
from src.objets.models import ObjetConnecte, CategorieObjet
from django.shortcuts import get_object_or_404
from src.utilisateurs.models import Utilisateur
from .forms import EditProfilForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, update_session_auth_hash

User = get_user_model()

@login_required
@role_required('simple')
def visualisation_home(request):
    # Page d'accueil du module visualisation
    return render(request, 'visualisation/home.html')

@login_required
@role_required('simple')
def visualisation_profil(request):
    # Pour la section "Mon Profil" et la liste des autres profils
    utilisateurs = Utilisateur.objects.exclude(id=request.user.id)
    return render(request, 'visualisation/profil.html', {'utilisateurs': utilisateurs})

@login_required
@role_required('simple')
def visualisation_objets(request):
    # Récupération des paramètres GET
    query = request.GET.get('q', '')             # terme de recherche
    etat_filter = request.GET.get('etat', '')    # filtre sur l'état
    cat_filter = request.GET.get('categorie', '') # filtre sur la catégorie

    # On récupère tous les objets
    objets = ObjetConnecte.objects.all()

    # Filtrage par recherche (nom ou description)
    if query:
        objets = objets.filter(
            Q(nom__icontains=query) |
            Q(description__icontains=query)
        )

    # Filtrage par état
    if etat_filter:
        objets = objets.filter(etat=etat_filter)

    # Filtrage par catégorie
    if cat_filter:
        objets = objets.filter(categorie__id=cat_filter)

    # Pour alimenter la liste déroulante des catégories
    categories = CategorieObjet.objects.all()

    context = {
        'objets': objets,
        'query': query,
        'etat': etat_filter,
        'categorie': cat_filter,
        'categories': categories,
    }
    return render(request, 'visualisation/objets_list.html', context)

@login_required
@role_required('simple')
def visualisation_objet_detail(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, id=objet_id)
    return render(request, 'visualisation/objet_detail.html', {'objet': objet})

@login_required
@role_required('simple')
def profil_home(request):
    # Affiche la page de profil de l'utilisateur connecté
    user_profile = request.user
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'visualisation/profil.html', {'user_profile': user_profile})

@login_required
@role_required('simple')
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

@login_required
@role_required('simple')
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

@login_required
@role_required('simple')
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

@login_required
@role_required('simple')
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

@login_required
@role_required('simple')
def view_profil(request, user_id):
    # Affiche le profil d'un autre membre
    user_profile = get_object_or_404(Utilisateur, id=user_id)
    return render(request, 'visualisation/view_profil.html', {'user_profile': user_profile})


@login_required
@role_required('simple')
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

@login_required
@role_required('simple')
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
@role_required('simple')
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

@login_required
@role_required('simple')
def objets_list(request):
    # Barre de recherche avec deux filtres : état et catégorie
    query = request.GET.get('q', '')
    etat_filter = request.GET.get('etat', '')
    categorie_filter = request.GET.get('categorie', '')

    objets = ObjetConnecte.objects.all()

    if query:
        objets = objets.filter(nom__icontains=query)
    if etat_filter:
        objets = objets.filter(etat=etat_filter)
    if categorie_filter:
        objets = objets.filter(categorie__id=categorie_filter)

    # Vous pouvez passer la liste des catégories dans le contexte si nécessaire
    from src.objets.models import CategorieObjet
    categories = CategorieObjet.objects.all()

    context = {
        'objets': objets,
        'query': query,
        'etat': etat_filter,
        'categorie': categorie_filter,
        'categories': categories,
    }
    return render(request, 'visualisation/objets_list.html', context)

