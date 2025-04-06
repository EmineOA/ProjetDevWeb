from src.utilisateurs.decorators import role_required
from django.shortcuts import render, get_object_or_404, redirect
from src.objets.models import ObjetConnecte

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

