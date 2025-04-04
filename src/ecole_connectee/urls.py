from django.contrib import admin
from django.urls import path, include
from .views import index

urlpatterns = [
    path('',index, name="index"),
    path('admin/', include('administration.urls')),
    path('objets/', include('src.objets.urls')),
    path('accounts/', include('django.contrib.auth.urls'))
    # Ajouter les autres routes selon les modules...
]
