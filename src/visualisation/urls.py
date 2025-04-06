from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualisation_home, name='visualisation_home'),
    path('objets/', views.visualisation_objets, name='visualisation_objets'),
    path('objet/<int:objet_id>/', views.visualisation_objet_detail, name='visualisation_objet_detail'),
    path('profil/', views.visualisation_profil, name='visualisation_profil'),
    path('profil/edit/', views.edit_profil, name='edit_profil'),
    path('profil/<int:user_id>/', views.view_profil, name='view_profil'),
    path('profil/search/', views.search_profiles, name='search_profils'),
    path('profils/', views.view_profiles, name='view_profiles'),
    path('profil/change_password/', views.change_password, name='change_password'),
    path('<int:user_id>/', views.view_profil, name='view_profil'),
    path('recherche/', views.visualisation_recherche_objet, name='visualisation_recherche_objet'),
]
