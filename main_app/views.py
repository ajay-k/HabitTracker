from django.shortcuts import render
from django.http import HttpResponse

class Habit:  # Note that parens are optional if not inheriting from another class
  def __init__(self, name, description, good):
    self.name = name
    self.description = description
    self.good = good

habits = [
  Habit('Exercise', 'Get out more', True),
  Habit('Read', 'Gain knowledge', True),
  Habit('Bite Nails', 'Stop bititng nails', False),
]

#Home view
def home(request):
  return render(request, 'home.html')

def habits_index(request):
  return render(request, 'habits.html', {'habits': habits})