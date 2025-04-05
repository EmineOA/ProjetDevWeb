from django.urls import path
from . import views

urlpatterns = [
    path('tableau/', views.visualisation_tableau, name='visualisation_tableau'),
    path('graphique/', views.visualisation_graphique, name='visualisation_graphique'),
]
