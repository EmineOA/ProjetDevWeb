from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_objets, name='objets_list'),
    path('add/', views.objet_add, name='objet_add'),
    path('<int:objet_id>/edit/', views.objet_edit, name='objet_edit'),
    path('<int:objet_id>/delete/', views.objet_delete, name='objet_delete'),
]
