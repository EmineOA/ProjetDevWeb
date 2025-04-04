from django import forms
from .models import ObjetConnecte

class ObjetConnecteForm(forms.ModelForm):
    class Meta:
        model = ObjetConnecte
        fields = ['nom', 'description', 'categorie', 'etat', 'salle', 'consommation_energetique', 'connectivite', 'image']
