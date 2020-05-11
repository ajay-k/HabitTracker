from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import Habit, HabitLogger
from .forms import HabitForm

#User imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

#Date imports
from datetime import datetime
from datetime import date
from django.http import JsonResponse


#Home view
def home(request):
  return render(request, 'home.html')

@login_required
def habits_index(request, selMonth=None, selDay=None, selYear=None):

  dt = datetime.today()
  if request.is_ajax():
    current_user = request.user
    habits = Habit.objects.all()
    habits = list(Habit.objects.filter(user_id=request.user).values())

    allDates = HabitLogger.objects.values_list('date', flat=True)
    all_dates_removed_dups = list(set(allDates)) 
    completedDates = []
    for date in all_dates_removed_dups:
      if(check_complete(request=request, formatedDate=date)==True):
        completedDates.append(date)

    return JsonResponse({"habits": habits, "completedDates": completedDates}, safe=False)  # or JsonResponse({'data': data})

  else:
    selMonth = datetime.now().month
    selDay = datetime.now().day
    selYear = datetime.now().year

  habit_logger_collection = HabitLogger.objects.filter(date__month=selMonth, date__day=selDay, date__year= selYear)

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
      return redirect('index')
  else:
    form = HabitForm()
  context = { 'form': form}
  return render(request, 'habits/habit_form.html', context)


@login_required
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
  if request.is_ajax():
    habit_id = request.GET.get('habit_id')
    habit = Habit.objects.get(id=habit_id)
    Habit.objects.get(id=habit_id).delete()
  return redirect('index')

def habit_complete(request, habit_id=None):
  if request.is_ajax():
    habit_id = request.GET.get('habit_id')
    selMonth = request.GET.get('selMonth')
    selDay = request.GET.get('selDay')
    selYear = request.GET.get('selYear')

    if(int(selMonth) < 10 ):
      selMonth = '0' + selMonth
    print(selMonth)

    if(int(selDay) < 10 ):
      selDay = '0' + selDay
    
    formatedDate = selYear + '-' + selMonth + '-' + selDay

    if(not(HabitLogger.objects.filter(habit_id=habit_id).filter(date=formatedDate).exists())):
        habit_logger = HabitLogger()
        habit = Habit.objects.get(id=habit_id)
        habit_logger.habit = habit
        habit_logger.user = request.user
        habit_logger.date = formatedDate
        habit_logger.current_total_habits =  Habit.objects.filter(user_id=request.user.id).count()
        habit.completed_count += 1
        habit.save()
        habit_logger.save()
        if(check_complete(request=request, formatedDate=formatedDate)==True):
          return JsonResponse({"status": "204", "formatedDate": formatedDate }, safe=False)
        return JsonResponse({"status": "200", "formatedDate": formatedDate }, safe=False)

  return JsonResponse({"status": "400", "formatedDate": formatedDate }, safe=False)

def check_complete(request, formatedDate):
    habit_id = request.GET.get('habit_id')
    selMonth = request.GET.get('selMonth')
    selDay = request.GET.get('selDay')
    selYear = request.GET.get('selYear')

    usr_val = list(HabitLogger.objects.filter(user_id=request.user.id).filter(date=formatedDate).values_list('current_total_habits', flat=True))[0]

    user_habits = Habit.objects.filter(user_id=request.user.id).count()

    habitLogger_count = HabitLogger.objects.filter(user_id=request.user.id).filter(date=formatedDate).count()
  
    if(usr_val <= habitLogger_count):
      return True
    return False

def profile_index(request):
  habits = Habit.objects.all()
  allDates = list(HabitLogger.objects.values_list('date', flat=True))
  allDates.sort()
  streak = 1
  highestStreak = 1

  for i in range(0, len(allDates)-1):

    if( (allDates[i].day + 1) == allDates[i+1].day):
      streak += 1
      if(highestStreak <= streak):
        highestStreak = streak
    else:
      streak = 1

  return render(request, 'profile.html', { 'habits': habits , 'highestStreak': highestStreak})

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

