from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import Habit
from .forms import HabitForm


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

def habits_index(request):
  habits = Habit.objects.all()
  return render(request, 'habits.html', {'habits': habits})

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
    
