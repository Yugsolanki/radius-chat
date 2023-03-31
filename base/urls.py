from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('room/', views.room, name='room'),
    path('createroom/', views.createroom, name='createroom')   
]
