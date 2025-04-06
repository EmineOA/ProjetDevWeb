from django.urls import path
from . import views

urlpatterns = [
    path('', views.gestion_home, name='gestion_home'),
    path('objets/', views.objets_list, name='gestion_objets_connectes'),
    path('export/', views.export_data_home, name='gestion_export_home'),
    path('export/csv/', views.export_data_csv, name='gestion_export_csv'),
    path('export/pdf/', views.export_data_pdf, name='gestion_export_pdf'),
    path('objets/add/', views.objet_add, name='objet_add'),
    path('objet/<int:objet_id>/edit/', views.objet_edit, name='objet_edit'),
    path('objet/request_delete/<int:objet_id>/', views.objet_request_delete, name='objet_request_delete'),
]
