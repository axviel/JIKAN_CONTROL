from django.shortcuts import render
from django.contrib import messages

from .models import Exam

import datetime

def exams(request):
  return render(request, 'exams/list.html')