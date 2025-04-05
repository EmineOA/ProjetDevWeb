from django.urls import path
from . import views

urlpatterns = [
    path('tableau/', views.visualisation_tableau, name='visualisation_tableau'),
    path('graphique/', views.visualisation_graphique, name='visualisation_graphique'),
    path('profil/', views.mon_profil, name='mon_profil'),
    path('rechercher-objet/', views.rechercher_objet_connecte, name='rechercher_objet'),
    path('objet/<int:objet_id>/', views.detail_objet, name='detail_objet'),


]
