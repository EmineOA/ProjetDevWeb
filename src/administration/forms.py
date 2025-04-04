# administration/forms.py
from django import forms
from src.utilisateurs.models import Utilisateur
from .models import Apparence

class UserAddForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'type_membre', 'xp']  # Remplacer role par type_membre

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['email', 'type_membre', 'xp']

class ApparenceForm(forms.ModelForm):
    class Meta:
        model = Apparence
        fields = ['theme_color', 'logo_url']
        widgets = {
            'theme_color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '#ffffff'}),
            'logo_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'http://...'}),
        }
