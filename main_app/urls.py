from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('habits/', views.habits_index, name='index'),
    path('habits/add/', views.habit_add, name ='habit_add'),
    path('habit/update/<int:habit_id>', views.habit_update, name='habit_update'),
    path('habit/delete/', views.habit_delete, name='habit_delete'),
    path('habit/complete/', views.habit_complete, name='habit_complete'),
    path('habits/check_complete/', views.check_complete, name='check_complete'),
    path('accounts/signup', views.signup, name='signup'),
]