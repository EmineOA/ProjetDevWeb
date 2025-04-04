from django.shortcuts import render, redirect, get_object_or_404
from .models import ObjetConnecte
from .forms import ObjetConnecteForm

def list_objets(request):
    objets = ObjetConnecte.objects.all()
    context = {'objets': objets}
    # Ici, on réutilise le template déjà conçu pour la gestion des objets
    return render(request, 'gestion_objets_avances.html', context)

def objet_add(request):
    if request.method == 'POST':
        form = ObjetConnecteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('objets_list')
    else:
        form = ObjetConnecteForm()
    return render(request, 'objet_add.html', {'form': form})

def objet_edit(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, id=objet_id)
    if request.method == 'POST':
        form = ObjetConnecteForm(request.POST, request.FILES, instance=objet)
        if form.is_valid():
            form.save()
            return redirect('objets_list')
    else:
        form = ObjetConnecteForm(instance=objet)
    return render(request, 'objet_edit.html', {'form': form, 'objet': objet})

def objet_delete(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, id=objet_id)
    if request.method == 'POST':
        objet.delete()
        return redirect('objets_list')
    return render(request, 'objet_delete_confirm.html', {'objet': objet})
