from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Note

import datetime

def index(request):
  if not request.user.is_authenticated:
      messages.error(request, 'Unauthorized. Must be logged in')
      return redirect('login')

  # Fetch notes from db
  notes = Note.objects.order_by('-created_date').filter(is_hidden=False)

  # Pagination
  paginator = Paginator(notes, 5)
  page = request.GET.get('page')
  paged_notes = paginator.get_page(page)

  # Data that is passed to the template
  context = {
    'notes': paged_notes
  }

  return render(request, 'notes/note_list.html', context)

def note(request, note_id):
  return render(request, 'notes/note_detail.html')

def search(request):
  return render(request, 'notes/note_search.html')