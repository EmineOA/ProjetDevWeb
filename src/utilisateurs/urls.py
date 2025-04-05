from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
