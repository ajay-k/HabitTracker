from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Habit(models.Model):
  name = models.CharField(max_length=100)
  goal = models.CharField(max_length=100)
  completed_count = models.IntegerField(default=0)
  isGood = models.BooleanField()

  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

class HabitLogger(models.Model):
  habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateField()
  current_total_habits = models.IntegerField(default=1)

  def __str__(self):
    return self.habit.name
