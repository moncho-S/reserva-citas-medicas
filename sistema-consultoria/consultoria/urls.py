"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', listadoView,name='listadoName'),
    path('login/', loginView,name='loginName'),
    path('logout/', logoutView,name='logoutName'),
    path('addDoctors/', agregarView,name='agregarName'),
    path('booking/<str:id>', reservarView,name='reservarName'),
    path('signup/', signupPacienteView,name='signupPacienteName'),
    path('appointments/', misReservasView,name='misReservasName'),
    path('appointments/delete/<str:id>', deleteReservasView,name='deleteReservasName'),
    path('appointments/confirm/<str:id>', confirmReservasView,name='confirmReservasName'),
    path('howto/', howToView,name='howToName'),
]
