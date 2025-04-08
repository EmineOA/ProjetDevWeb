# administration/forms.py
from django import forms
from src.utilisateurs.models import Utilisateur
from .models import Apparence
from django.core.exceptions import ValidationError

class UserAddForm(forms.ModelForm):
    # Champs pour le mot de passe, on les ajoute manuellement
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
        help_text="Saisissez le mot de passe."
    )
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput,
        help_text="Confirmez le mot de passe."
    )

    class Meta:
        model = Utilisateur
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'pseudo',
            'age',
            'sexe',
            'date_naissance',
            'photo',
            'type_membre',
            'xp',
            'niveau',
        ]
        # Vous pouvez ajouter des widgets si besoin pour personnaliser l'affichage

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        # Créer l'instance sans l'enregistrer immédiatement
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

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
        fields = ['logo', 'background_color']
        widgets = {
            'logo': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'http://...'}),
            'background_color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '#ffffff'}),
        }

