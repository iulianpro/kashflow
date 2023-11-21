from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home-validate/', views.home_validate, name='home-validate'),
    path('home-authenticated/', views.home_authenticated, name='home-authenticated'),
]
