from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',include('src.information.urls')),
    path('admin/', include('src.administration.urls')),
    path('objets/', include('src.objets.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('inscription/', include('src.utilisateurs.urls')),
    path('information/', include('src.information.urls')),
    path('visualisation/', include('src.visualisation.urls')),
    path('gestion/', include('src.gestion.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
