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
        # Vous pouvez ajuster cette liste pour inclure tous les champs que vous souhaitez rendre modifiables.
        # Par exemple, ici j'inclus username, first_name, last_name, email, age, sexe, date_naissance, type_membre, photo, xp, et niveau.
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'age',
            'sexe',
            'date_naissance',
            'type_membre',
            'photo',
            'xp',
            'niveau',
            'est_verifie'
        ]

class ApparenceForm(forms.ModelForm):
    class Meta:
        model = Apparence
        fields = ['background_color', 'logo']
        widgets = {
            'background_color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '#ffffff'
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }

