from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import Habit, HabitLogger
from .forms import HabitForm, HabitLoggerForm

#User imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from datetime import datetime
from datetime import date
from django.http import JsonResponse




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
def habits_index(request, selMonth=None, selDay=None, selYear=None):
  print(selMonth)
  print(selDay)
  print(selYear)
  # print("Incoming Data: ")
  # print(month)
  # print(day)
  # print(year)
  dt = datetime.today()
  if  request.is_ajax():
    selMonth = request.GET.get('selMonth')
    selDay = request.GET.get('selDay')
    selYear = request.GET.get('selYear')

    current_user = request.user
    print("Current USER ID: " + str(current_user.id))
    # habit_logger_collection = HabitLogger.objects.filter(date__month=selMonth, date__day=selDay, date__year= selYear)
    data = list(HabitLogger.objects.filter(date__month=selMonth, date__day=selDay, date__year= selYear).values().filter(user_id=current_user.id))  # wrap in list(), because QuerySet is not JSON serializable
    print(data)
    print("---------------")
    myData = []
    for item in data:
      print(item['habit_id'])
      myHab = list(Habit.objects.filter(id=item['habit_id']).values())
      myData.append(myHab)
      # print(myHab)
    print(list(myData))
    return JsonResponse(list(myData), safe=False)  # or JsonResponse({'data': data})

  else:
    selMonth = datetime.now().month
    selDay = datetime.now().day
    selYear = datetime.now().year

  habit_logger_collection = HabitLogger.objects.filter(date__month=selMonth, date__day=selDay, date__year= selYear)
  print(habit_logger_collection)

  return render(request, 'habits.html', {'habit_logger_collection': habit_logger_collection})

@login_required
def habit_add(request):
  habit_logger = HabitLogger()
  if request.method == 'POST':
    form = HabitForm(request.POST)
    if form.is_valid():
      habit = form.save(commit=False)
      habit.user = request.user
      habit.save()
      habit_logger.habit = habit
      habit_logger.user = request.user
      habit_logger.date = datetime.date
      habit_logger.save()
      return redirect('index')
  else:
    form = HabitForm()
  context = { 'form': form}
  return render(request, 'habits/habit_form.html', context)

def habit_update(request, habit_id):
  habit = Habit.objects.get(id=habit_id)
  if request.method == 'POST':
    form = HabitForm(request.POST, instance=habit)
    if form.is_valid():
      habit = form.save()
      return redirect('index')
  else: 
    form = HabitForm(instance=habit)
  context = { 'form': form }
  return render(request, 'habits/habit_form.html', { 'form': form })

def habit_delete(request, habit_id=None):
  if  request.is_ajax():
    print("AJAX Incoming")
    habit_id = request.GET.get('habit_id')
  # print("-----Yo------------")
  # url = request.get_full_path() 
  # urlSplit = url.split('/')
  # print(urlSplit)
  # habit_id = urlSplit[-1]
  print(habit_id)
  print('-------dfdds----')


  habit = Habit.objects.get(id=habit_id)
  Habit.objects.get(id=habit_id).delete()
  return redirect('index')




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
    
