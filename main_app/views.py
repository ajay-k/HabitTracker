from django.shortcuts import render
from django.http import HttpResponse

#Home view
def home(request):
  return render(request, 'home.html')
