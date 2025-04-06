from django import forms
from src.utilisateurs.models import Utilisateur
from django.contrib.auth.forms import UserChangeForm

class EditProfilForm(UserChangeForm):
    password = None  # Supprime le champ password

    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email', 'photo']  # Ajoutez d'autres champs si nécessaire
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
