# src/information/views.py
from django.shortcuts import render

def information_home(request):
    # On initialise error_message à None
    error_message = None

    # Exemple de condition d'erreur : si l'utilisateur n'est pas authentifié, on affiche un message d'information
    if not request.user.is_authenticated:
        error_message = "Vous n'êtes pas connecté. Certaines fonctionnalités pourraient être limitées."

    # Exemple de données adaptées à une école
    actualites = [
        {"titre": "Rentrée 2025", "contenu": "La rentrée scolaire aura lieu le 5 septembre 2025."},
        {"titre": "Nouveau programme", "contenu": "Découvrez le nouveau programme d'enseignement pour l'année."},
        {"titre": "Festival Scolaire", "contenu": "Le festival annuel se déroulera le 15 octobre."},
    ]
    menu_jour = "Aujourd'hui : Poulet rôti, riz, légumes, dessert au yaourt."
    horaires = "L'école est ouverte du lundi au vendredi, de 8h00 à 18h00."

    context = {
        "actualites": actualites,
        "menu_jour": menu_jour,
        "horaires": horaires,
        "error_message": error_message,
    }
    return render(request, 'information/home.html', context)



def information_search(request):
    query = request.GET.get('q', '')
    filtre_categorie = request.GET.get('categorie', '')

    # Exemple de résultats cohérents pour une école
    resultats = [
        {"titre": "Journée portes ouvertes",
         "description": "Venez découvrir notre école lors de la journée portes ouvertes."},
        {"titre": "Conférence sur l'innovation pédagogique",
         "description": "Une conférence organisée par des experts du secteur."},
        {"titre": "Sortie éducative au musée",
         "description": "Préparez-vous pour une sortie éducative exceptionnelle au musée."},
    ]

    context = {
        "query": query,
        "categorie": filtre_categorie,
        "resultats": resultats,
    }
    return render(request, 'information/results.html', context)
