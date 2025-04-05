from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualisation_home, name='visualisation_home'),
    path('profil/', views.visualisation_profil, name='visualisation_profil'),
    path('objets-connectes/', views.visualisation_objets, name='visualisation_objets'),
]
