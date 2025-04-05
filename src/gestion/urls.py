from django.urls import path
from . import views

urlpatterns = [
    path('', views.gestion_home, name='gestion_home'),
    path('objets/', views.gestion_objets, name='gestion_objets'),
    path('export/', views.export_data, name='export_data'),
]
