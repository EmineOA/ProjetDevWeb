# src/information/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.information_home, name='information_home'),
    path('search/', views.information_search, name='information_search'),
]
