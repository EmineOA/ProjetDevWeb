from django.urls import path
from . import views

urlpatterns = [
    path('', views.tableau_de_bord, name='tableau_de_bord'),
    path('gestion-utilisateurs/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    path('gestion-objets-avances/', views.gestion_objets_avances, name='gestion_objets_avances'),
    path('securite-maintenance/', views.securite_maintenance, name='securite_maintenance'),
    path('personnalisation/', views.personnalisation, name='personnalisation'),
    path('rapports-avances/', views.rapports_avances, name='rapports_avances'),
    path('gestion-utilisateurs/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    path('gestion-utilisateurs/add/', views.user_add, name='user_add'),
    path('gestion-utilisateurs/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('gestion-utilisateurs/<int:user_id>/delete/', views.user_delete, name='user_delete'),
]
