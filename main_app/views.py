from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import Habit
from .forms import HabitForm

#User imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# class Habit:  # Note that parens are optional if not inheriting from another class
#   def __init__(self, name, description, good):
#     self.name = name
#     self.description = description
#     self.good = good

# habits = [
#   Habit('Exercise', 'Get out more', True),
#   Habit('Read', 'Gain knowledge', True),
#   Habit('Bite Nails', 'Stop bititng nails', False),
# ]

#Home view
def home(request):
  return render(request, 'home.html')

@login_required
def habits_index(request):
  habits = Habit.objects.filter(user=request.user)
  return render(request, 'habits.html', {'habits': habits})

@login_required
def add_habit(request):
  if request.method == 'POST':
    form = HabitForm(request.POST)
    if form.is_valid():
      habit = form.save(commit=False)
      habit.user = request.user
      habit.save()
      return redirect('index')
  else:
    form = HabitForm()
  context = { 'form': form}
  return render(request, 'habits/habit_form.html', context)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid signup - try again'
  form = UserCreationForm()
  context = { 'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
    
