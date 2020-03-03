from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Exam

import datetime

def index(request):
  # Fetch exams from db
  exams = Exam.objects.order_by('-created_date').filter(is_hidden=False)

  # Pagination
  paginator = Paginator(exams, 5)
  page = request.GET.get('page')
  paged_exams = paginator.get_page(page)

  # Data that is passed to the template
  context = {
    'exams': paged_exams
  }

  return render(request, 'exams/exam_list.html', context)

def exam(request, exam_id):
  return render(request, 'exams/exam_detail.html')

def search(request):
  return render(request, 'exams/exam_search.html')