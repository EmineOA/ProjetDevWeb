from django.contrib import admin
from django.urls import path, include
from .views import index

urlpatterns = [
    path('',index, name="index"),
    path('admin/', include('src.administration.urls')),
    path('objets/', include('src.objets.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('inscription/', include('src.utilisateurs.urls')),
    path('information/', include('src.information.urls')),
    path('visualisation/', include('src.visualisation.urls')),
    path('gestion/', include('src.gestion.urls')),
    # Ajouter les autres routes selon les modules...
]
