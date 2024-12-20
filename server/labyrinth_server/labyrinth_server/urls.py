"""
URL configuration for labyrinth_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from labyrinth.interfaces.register_adventurer import RegisterAdventurerView
from labyrinth.interfaces.load_labyrinth import LabyrinthView
from labyrinth.interfaces.navigate_labyrinth import NavigateLabyrinthView

urlpatterns = [
    path('register/', RegisterAdventurerView.as_view()),
    path('labyrinth/', LabyrinthView.as_view()),
    path('labyrinth/navigate/<str:adventurer_name>/', NavigateLabyrinthView.as_view()),
]
