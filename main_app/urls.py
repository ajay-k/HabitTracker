from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('habits/', views.habits_index, name='index'),
    path('habits/add/', views.habit_add, name ='habit_add'),
    path('habit/update/<int:habit_id>', views.habit_update, name='habit_update'),
    path('habit/delete/<int:habit_id>', views.habit_delete, name='habit_delete'),
    path('accounts/signup', views.signup, name='signup'),
]