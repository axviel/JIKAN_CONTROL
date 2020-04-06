from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse

from .models import Note
from .forms import NotesForm

from events.models import Event
from exams.models import Exam

import datetime
import json

def index(request):
  # Fetch exams from db
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


# Returns the detail info of a Note. Also used to create and update notes
def note(request, note_id=0):
  if request.method == "POST":
    # Kick user if not logged in
    if not request.user.is_authenticated:
      messages.error(request, 'Unauthorized. Must be logged in')
      return redirect('note_list')

    # Get the POST form
    form = NotesForm(request.POST)

    if form.is_valid():
      note_id = form.cleaned_data['note_id']
      title = form.cleaned_data['title']
      description = form.cleaned_data['description']
      created_date = datetime.date.today()
      events_id = request.POST['event_id']

      event_id = get_object_or_404(Event, pk=events_id)

      # Searches the db for a note with the id and updates it. if not found, creates a new exam and returns is_created=True
      note, is_created = Note.objects.update_or_create(
          id=note_id,
          defaults={
            'user_id': request.user.id,
            'title': title,
            'description': description,
            'created_date': created_date,
	    'events_id': events_id
       },
      )

      # Save in the db
      note.save()

      # If note was created via calendar page, return the id
      if 'is_calendar_form' in request.POST:
        context = {
          'note_id': note.id,
          'title': note.title,
          'created_date': created_date,
	  'event_id': event_id
        }
        context = json.dumps(context)
        return HttpResponse(context)

      # UI success message
      messages.success(request, 'Note created successfully')

      # If it was updated return the page and form
      if not is_created:
        context = {
          'form': form
        }
        return render(request, 'notes/note_detail.html', context)

      # If it was created, redirect to url with id
      return redirect('note_detail', note_id=note.id) #redirect(url path name, id specified in the path)

    # Form was invalid, so return it
    context = {
      'form': form
    }

    # UI error message
    messages.error(request, 'Note was not created')

    return render(request, 'notes/note_detail.html', context)

  else:

    # If GET request came from calendar
    if 'is_calendar_form' in request.GET:
      event_id = request.GET['event_id']
      note = Note.objects.get(id=note_id)

      context = {
        'note_id': note.id,
        'user_id': note.user_id,
        'title': note.title,
        'description': note.description,
        'created_date': note.created_date
      }
      context = json.dumps(context, indent=4, sort_keys=True, default=str)

      return HttpResponse(context)

    if not request.user.is_authenticated:
      messages.error(request, 'Access denied. Must be logged in')
      return redirect('note_list') #redirect(url path name)

    # If viewing detail of an existing note, fill the form with its values. if not, show form with blank and default values
    context = {}

    if note_id > 0:
      note = get_object_or_404(Note, pk=note_id)

      form = NotesForm(initial={
        'note_id': note.id,
        'user_id': note.user_id,
        'title': note.title,
        'description': note.description,
        'created_date': note.created_date
      })
      # Get exam notes and events
      exams = Exam.objects.all().filter(event_id=note.events_id,is_hidden=False)
      events = Event.objects.all().filter(id=note.events_id,is_hidden=False)

      context['form'] = form
      context['exams'] = exams
      context['events'] = events

    else:
      form = NotesForm(initial={
        'created_date': datetime.date.today()
      })

      context['form'] = form

    return render(request, 'notes/note_detail.html', context)

# Search for notes 
def search(request):
  queryset_list = Note.objects.order_by('-created_date')

  # Title
  if 'title' in request.GET:
    title = request.GET['title']
    # Check if empty string
    if title:
      # Search title for anything that matches a keyword
      queryset_list = queryset_list.filter(title__icontains=title)

  context = {
    'notes': queryset_list,
  }

  # Request contains at least one form field, return the form with its field values
  if 'title' in request.GET:
    form = NotesForm(initial={
	  'events_id': request.GET.get('events_id'),
          'title': request.GET['title'],
          'created_date': request.GET['created_date'],
        })

    search_form_defaults(form)

    context['form'] = form

  # Request does not contain form submission, return empty form
  else:
    form = NotesForm()

    search_form_defaults(form)

    context['form'] = form


  return render(request, 'notes/note_search.html', context)

# Marks a note as hidden
def remove(request):
  if request.method == 'POST':
    note_id = request.POST['note_id']

    note = Note.objects.get(id=note_id)
    note.is_hidden = True
    note.save()

    if 'is_detail' in request.POST:
      return redirect('note_list')
    else:
      return HttpResponse('')


# Marks are required fields as not required and adds an 'Any' value to the drop down lists
def search_form_defaults(form):
  form.fields['title'].required = False
  form.fields['created_date'].required = False
