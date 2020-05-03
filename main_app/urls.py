from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('habits/', views.habits_index, name='index'),
    path('habits/add/', views.add_habit, name ='add_habit'),
    path('accounts/signup', views.signup, name='signup'),
]