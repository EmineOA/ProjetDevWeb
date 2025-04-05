from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Utilisateur

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
    photo = forms.ImageField(
        required=False,
        label="Photo de profil",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = Utilisateur
        fields = ("pseudo", "email", "age", "sexe", "date_naissance", "photo", "password1", "password2")

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        # Séparez les champs publics et privés si nécessaire
        fields = ['pseudo', 'age', 'sexe', 'date_naissance', 'photo', 'first_name', 'last_name', 'email']
        widgets = {
            'pseudo': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

