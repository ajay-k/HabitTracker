from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Habit(models.Model):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=100)
  isGood = models.BooleanField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

class HabitLogger(models.Model):
  habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateField()
  completed = models.BooleanField()

  def __str__(self):
    return self.habit.name
