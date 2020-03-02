from django.shortcuts import render
from django.contrib import messages

from .models import Note

import datetime

def notes(request):
  return render(request, 'notes/list.html')