from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from src.utilisateurs.models import Utilisateur

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    pseudo = forms.CharField(
        max_length=100,
        required=True,
        label="Pseudo",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    age = forms.IntegerField(
        required=False,
        min_value=0,
        label="Âge",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    sexe = forms.ChoiceField(
        choices=[('', 'Choisir...'), ('Homme', 'Homme'), ('Femme', 'Femme')],
        required=False,
        label="Sexe/Genre",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_naissance = forms.DateField(
        required=False,
        label="Date de naissance",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    type_membre = forms.CharField(
        max_length=50,
        required=False,
        label="Type de membre",
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Ex: étudiant, agent de maintenance, membre de l\'administration'})
    )
    photo = forms.ImageField(
        required=False,
        label="Photo de profil",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = Utilisateur
        fields = ("pseudo", "email", "age", "sexe", "date_naissance", "type_membre", "photo", "password1", "password2")