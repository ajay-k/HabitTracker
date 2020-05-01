from django.db import models

# Create your models here.

class Habit(models.Model):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=100)
  isGood = models.BooleanField()

  def __str__(self):
    return self.name