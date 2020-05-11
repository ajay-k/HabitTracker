from django import forms
from .models import Habit, HabitLogger

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ('name', 'goal', 'isGood')

