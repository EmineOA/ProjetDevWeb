from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualisation_home, name='visualisation_home'),
    path('objet/<int:objet_id>/', views.objet_detail, name='objet_detail'),
    path('profil/', views.profil, name='profil'),
    path('profil/modifier/', views.modifier_profil, name='modifier_profil'),
    path('recherche/', views.visualisation_recherche_objet, name='visualisation_recherche_objet'),
]
