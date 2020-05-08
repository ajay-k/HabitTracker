from django.contrib import admin

from .models import Habit, HabitLogger
# Register your models here.



# Register your models here
admin.site.register(Habit)
admin.site.register(HabitLogger)