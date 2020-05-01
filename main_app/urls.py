from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('habits/', views.habits_index, name='index'),
]
