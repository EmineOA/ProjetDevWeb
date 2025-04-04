# administration/forms.py
from django import forms
from src.utilisateurs.models import Utilisateur

class UserAddForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'type_membre', 'xp']  # Remplacer role par type_membre

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['email', 'type_membre', 'xp']
