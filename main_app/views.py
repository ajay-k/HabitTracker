from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import Habit, HabitLogger
from .forms import HabitForm

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
  if request.is_ajax():
    # selMonth = request.GET.get('selMonth')
    # selDay = request.GET.get('selDay')
    # selYear = request.GET.get('selYear')

    current_user = request.user
    habits = Habit.objects.all()
    habits = list(Habit.objects.filter(user_id=request.user).values())
    print(habits)
    # print("Current USER ID: " + str(current_user.id))
    # # habit_logger_collection = HabitLogger.objects.filter(date__month=selMonth, date__day=selDay, date__year= selYear)
    # data = list(HabitLogger.objects.filter(date__month=selMonth, date__day=selDay, date__year= selYear).values().filter(user_id=current_user.id))  # wrap in list(), because QuerySet is not JSON serializable
    # print(data)
    # print("---------------")
    # myData = []
    # for item in data:
    #   print(item['habit_id'])
    #   myHab = list(Habit.objects.filter(id=item['habit_id']).values())
    #   myData.append(myHab)
    #   # print(myHab)
    # print(list(myData))
    print("************************")
    allDates = HabitLogger.objects.values_list('date', flat=True)
    print("DATES:")
    print(allDates)
    removedDups = list(set(allDates)) 
    completedDates = []
    print("//////////////////////")
    # .filter(user_id=request.user.id).filter(date=formatedDate).count()
    habitLogger_count = HabitLogger.objects.filter(user_id=request.user.id).filter(date='2020-05-14').count()
    print(request.user.id)
    print("PRINTING ALL OBJECTS")
    print(habitLogger_count)
    for date in removedDups:
      print(date)
      if(check_complete(request=request, formatedDate=date)==True):
        completedDates.append(date)
    print("COMPLETED DATES ARRAY: ")
    print(completedDates)
    return JsonResponse({"habits": habits, "completedDates": completedDates}, safe=False)  # or JsonResponse({'data': data})

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
      # habit_logger.habit = habit
      # habit_logger.user = request.user
      # habit_logger.date = datetime.date
      # habit_logger.save()
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

# TODO: Fix if statement
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

def habit_complete(request, habit_id=None):
  if request.is_ajax():
    print("AJAX Incoming")
    habit_id = request.GET.get('habit_id')
    selMonth = request.GET.get('selMonth')
    selDay = request.GET.get('selDay')
    selYear = request.GET.get('selYear')

    elemDate = selYear + '-' + selMonth + '-' + selDay

    if(int(selMonth) < 10 ):
      selMonth = '0' + selMonth
    print(selMonth)

    if(int(selDay) < 10 ):
      selDay = '0' + selDay
    
    
    formatedDate = selYear + '-' + selMonth + '-' + selDay

    print("DATE")
    print(formatedDate)
    print(HabitLogger.objects.filter(date=formatedDate).exists())
    # habit = Habit()
    # print(habit)
    # habit = Habit.objects.filter(id=habit_id)
    print("Habit Incoming!")
    if(not(HabitLogger.objects.filter(habit_id=habit_id).filter(date=formatedDate).exists())):
      # if(not(HabitLogger.objects.filter(date=formatedDate).exists())):
        print("I'm inside the if statement")
        habit_logger = HabitLogger()
        habit = Habit.objects.get(id=habit_id)
        habit_logger.habit = habit
        habit_logger.user = request.user
        habit_logger.date = formatedDate
        habit_logger.save()
        if(check_complete(request=request, formatedDate=elemDate)==True):
          return JsonResponse({"status": "204", "formatedDate": formatedDate }, safe=False)
        return JsonResponse({"status": "200", "formatedDate": formatedDate }, safe=False)

    # print(habit)
    # habit = Habit.objects.filter(id=habit_id)
    # habits = Habit()
    # print(type(habit))
    # print(type(habits))
    # print(type(a))

  # print("-----Yo------------")
  # url = request.get_full_path() 
  # urlSplit = url.split('/')
  # print(urlSplit)
  # habit_id = urlSplit[-1]
  print(habit_id)
  print('-------Udate----')

  return JsonResponse({"status": "400", "formatedDate": formatedDate }, safe=False)

def check_complete(request, formatedDate):
    print("I'm in check_complete function")
    habit_id = request.GET.get('habit_id')
    selMonth = request.GET.get('selMonth')
    selDay = request.GET.get('selDay')
    selYear = request.GET.get('selYear')
    # if(int(selMonth) < 10 ):
    #   selMonth = '0' + selMonth
    # print(selMonth)

    # if(int(selDay) < 10 ):
    #   selDay = '0' + selDay
    
    # formatedDate = selYear + '-' + selMonth + '-' + selDay
    user_habits = Habit.objects.filter(user_id=request.user.id).count()
    print("User Habits Count:")
    print(user_habits)

    print("USERID/FORMATTED DATE: ")
    print(request.user.id)
    print(formatedDate)
    habitLogger_count = HabitLogger.objects.filter(user_id=request.user.id).filter(date=formatedDate).count()
    print("HabitLogger Count")
    print(habitLogger_count)

    if(user_habits <= habitLogger_count):
      print("YES! EXACT")
      return True
    return False





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

def profile_index(request):
  pass
  return render(request, 'profile.html')

    