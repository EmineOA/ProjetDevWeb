import csv
import io
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from src.objets.models import ObjetConnecte
from src.objets.forms import ObjetConnecteForm

def gestion_home(request):
    """Page d'accueil du module Gestion, style similaire à celui de l'administration."""
    return render(request, 'gestion/home.html')

def objets_list(request):
    """Liste des objets connectés."""
    objets = ObjetConnecte.objects.all()
    context = {'objets': objets}
    return render(request, 'gestion/gestion_objets_connectes.html', context)

def export_data_home(request):
    return render(request, 'gestion/export_data_home.html')


def export_data_csv(request):
    """Exportation des objets en CSV."""
    objets = ObjetConnecte.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="objets.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nom', 'Catégorie', 'État', 'Salle', 'Consommation'])
    for obj in objets:
        writer.writerow([
            obj.id,
            obj.nom,
            obj.categorie.nom if obj.categorie else 'N/A',
            obj.etat,
            obj.salle.nom if obj.salle else 'N/A',
            obj.consommation_energetique,
        ])
    return response

def export_data_pdf(request):
    """Exportation des objets en PDF."""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Objets Connectés - Export PDF")
    y -= 30
    p.setFont("Helvetica", 12)
    objets = ObjetConnecte.objects.all().order_by('id')
    for obj in objets:
        if y < 100:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 12)
        p.drawString(50, y, f"ID: {obj.id} - Nom: {obj.nom}")
        y -= 20
        cat = obj.categorie.nom if obj.categorie else 'N/A'
        sal = obj.salle.nom if obj.salle else 'N/A'
        p.drawString(50, y, f"Catégorie: {cat}, État: {obj.etat}, Salle: {sal}, Conso: {obj.consommation_energetique}")
        y -= 40
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="objets.pdf"'
    return response

def objet_add(request):
    """Ajout d’un nouvel objet."""
    if request.method == 'POST':
        form = ObjetConnecteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Objet ajouté avec succès.")
            return redirect('gestion_objets_connectes')
    else:
        form = ObjetConnecteForm()
    return render(request, 'gestion/objet_add.html', {'form': form})

def objet_edit(request, objet_id):
    """Modification d’un objet existant."""
    objet = get_object_or_404(ObjetConnecte, id=objet_id)
    if request.method == 'POST':
        form = ObjetConnecteForm(request.POST, request.FILES, instance=objet)
        if form.is_valid():
            form.save()
            messages.success(request, "Objet modifié avec succès.")
            return redirect('gestion_objets_connectes')
    else:
        form = ObjetConnecteForm(instance=objet)
    return render(request, 'objet_edit.html', {'form': form, 'objet': objet})

def objet_request_delete(request, objet_id):
    from src.objets.models import DemandeSuppressionObjet  # Assurez-vous que c'est bien importé ici
    objet = get_object_or_404(ObjetConnecte, id=objet_id)
    if request.method == 'POST':
        # Vérifier s'il existe déjà une demande pour cet objet par cet utilisateur (optionnel)
        if not DemandeSuppressionObjet.objects.filter(objet=objet, utilisateur=request.user, status='en attente').exists():
            DemandeSuppressionObjet.objects.create(
                objet=objet,
                utilisateur=request.user,
                raison="Demande de suppression initiée par l'utilisateur.",
                status='en attente'
            )
            messages.success(request, f"Votre demande de suppression pour l'objet {objet.nom} a été envoyée à l'administrateur.")
        else:
            messages.info(request, f"Vous avez déjà une demande de suppression en attente pour cet objet.")
        # Rediriger vers la liste des objets (assurez-vous que l'URL correspond bien à celle définie dans urls.py)
        return redirect('gestion_objets_connectes')
    return render(request, 'gestion/objet_delete_confirm.html', {'objet': objet})
