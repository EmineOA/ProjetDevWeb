import csv
import io
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .forms import UserAddForm, UserUpdateForm
from src.utilisateurs.decorators import role_required
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from src.utilisateurs.models import Utilisateur
from src.objets.models import ObjetConnecte, Rapport
from .forms import ApparenceForm
from .models import Apparence

@login_required
@role_required('administration')
def tableau_de_bord(request):
    context = {}
    return render(request, 'tableau_de_bord.html', context)

@login_required
@role_required('visualisation')
def gestion_utilisateurs(request):
    utilisateurs = Utilisateur.objects.all()
    context = {'utilisateurs': utilisateurs}
    return render(request, 'gestion_utilisateurs.html', context)

@login_required
@role_required('gestion')
def gestion_objets_avances(request):
    objets = ObjetConnecte.objects.all()
    context = {'objets': objets}
    return render(request, 'gestion_objets_avances.html', context)

def admin_required(user):
    return user.is_superuser or (user.is_authenticated and user.type_membre == 'administrateur')

@login_required
@user_passes_test(admin_required)
def securite_maintenance(request):
    """
    Vue pour la mise à jour du mot de passe admin.
    L'utilisateur doit fournir son ancien mot de passe, le nouveau et sa confirmation.
    Une fois le mot de passe modifié, l'utilisateur est déconnecté et invité à se reconnecter.
    """
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
            messages.success(request, "Votre mot de passe a été mis à jour. Veuillez vous reconnecter.")
            # Déconnecte l'utilisateur
            logout(request)
            return redirect('login')

    return render(request, 'securite_maintenance.html')

def personnalisation(request):
    # Tente de récupérer l'instance d'apparence, sinon en crée une nouvelle (identifiée par id=1)
    instance, created = Apparence.objects.get_or_create(id=1)
    if request.method == 'POST':
        form = ApparenceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('personnalisation')
    else:
        form = ApparenceForm(instance=instance)
    context = {'form': form}
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

@login_required
@user_passes_test(admin_required)
def backup_db(request):
    db_settings = settings.DATABASES['default']
    # Utilisez le chemin complet vers mysqldump fourni par WampServer
    mysqldump_path = r'D:\WampServer\bin\mysql\mysql9.1.0\bin\mysqldump.exe'  # Adaptez selon votre version
    cmd = [
        mysqldump_path,
        '-h', db_settings.get('HOST', 'localhost'),
        '-u', db_settings.get('USER', 'root'),
        f"--password={db_settings.get('PASSWORD', '')}",
        db_settings['NAME']
    ]
    try:
        dump = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        return HttpResponse("Erreur lors de la sauvegarde de la base de données.", status=500)

    response = HttpResponse(dump, content_type='application/sql')
    response['Content-Disposition'] = 'attachment; filename="backup.sql"'
    return response

def personnalisation(request):
    # Tente de récupérer l'instance d'apparence, sinon en crée une nouvelle (utilisation d'un identifiant fixe, ex: 1)
    instance, created = Apparence.objects.get_or_create(id=1)
    if request.method == 'POST':
        form = ApparenceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            # Optionnel : ajouter un message de succès
            return redirect('personnalisation')
    else:
        form = ApparenceForm(instance=instance)
    context = {'form': form}
    return render(request, 'personnalisation.html', context)


def export_reports_csv(request):
    # Création d'une réponse HTTP avec le type de contenu CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rapports.csv"'

    writer = csv.writer(response)
    # Écriture de l'en-tête
    writer.writerow(['ID', 'Titre', 'Contenu', 'Date de Création', 'Type de Rapport'])

    rapports = Rapport.objects.all().order_by('date_creation')
    for rapport in rapports:
        writer.writerow([
            rapport.id,
            rapport.titre,
            rapport.contenu,
            rapport.date_creation,
            rapport.type_rapport
        ])
    return response

def export_reports_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Rapports")
    y -= 30
    p.setFont("Helvetica", 12)

    rapports = Rapport.objects.all().order_by('date_creation')
    for rapport in rapports:
        if y < 100:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 12)
        p.drawString(50, y, f"ID: {rapport.id} - Titre: {rapport.titre}")
        y -= 20
        p.drawString(50, y, f"Date: {rapport.date_creation} - Type: {rapport.type_rapport}")
        y -= 20
        # Afficher un extrait du contenu pour éviter d'avoir trop de texte sur une seule page
        extrait = rapport.contenu[:100] + "..." if len(rapport.contenu) > 100 else rapport.contenu
        p.drawString(50, y, f"Contenu: {extrait}")
        y -= 30

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapports.pdf"'
    return response
