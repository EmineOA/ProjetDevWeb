from django.urls import path
from . import views
from .views import logout_confirm

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
path("logout/confirm/", logout_confirm, name="logout_confirm")

]
