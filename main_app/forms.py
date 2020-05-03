from django import forms
from .models import Habit

# name the form and inherit functionality from forms.ModelForm
class HabitForm(forms.ModelForm):
		# The Meta class is where we connect to a model and define
		# the fields that make up the form
    class Meta:
        model = Habit
        fields = ('name', 'description', 'isGood')