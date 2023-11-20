from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home-auth/', views.home_auth, name='home-auth'),
]
