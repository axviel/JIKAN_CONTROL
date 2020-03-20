from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse

from .models import Exam
from .forms import ExamForm

from events.models import Event
from notes.models import Note
from exams.models import Exam

import datetime
import json

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


# Returns the detail info of an Exam. Also used to create and update exams
def exam(request, exam_id=0):
  if request.method == "POST":
    # Kick user if not logged in
    if not request.user.is_authenticated:
      messages.error(request, 'Unauthorized. Must be logged in')
      return redirect('exam_list')

    # Get the POST form
    form = ExamForm(request.POST)

    if form.is_valid():
      exam_id = form.cleaned_data['exam_id']
      title = form.cleaned_data['title']
      description = form.cleaned_data['description']
      exam_number = form.cleaned_data['exam_number']
      event_id = 2
      predicted_study_hours = 0
      predicted_weeks = 0
      predicted_score = 0
      final_study_hours = 0
      final_weeks = 0
      final_score = 0
      created_date = datetime.date.today()

      # Searches the db for an exam with the id and updates it. if not found, creates a new exam and returns is_created=True
      exam, is_created = Exam.objects.update_or_create(
          id=exam_id,
          defaults={
            'user_id': request.user.id,
            'title': title,
            'description': description,
            'exam_number': exam_number,
            'predicted_study_hours': predicted_study_hours,
            'predicted_weeks': predicted_weeks,
            'predicted_score': predicted_score,
            'final_study_hours': final_study_hours,
            'final_weeks': final_weeks,
            'final_score': final_score,
            'created_date': created_date,
            'event_id': event_id
            },
      )

      # Save in the db
      exam.save()

      # If exam was created via calendar page, return the id
      if 'is_calendar_form' in request.POST:
        context = {
          'exam_id': exam.id,
          'title': exam.title,
          'start_time': exam.start_time.strftime("%H:%M")
        }
        context = json.dumps(context)
        return HttpResponse(context)

      # UI success message
      messages.success(request, 'Exam created successfully')

      # If it was updated return the page and form
      if not is_created:
        context = {
          'form': form
        }
        return render(request, 'exams/exam_detail.html', context)

      # If it was created, redirect to url with id
      return redirect('exam_detail', exam_id=exam.id) #redirect(url path name, id specified in the path)

    # Form was invalid, so return it
    context = {
      'form': form
    }

    # UI error message
    messages.error(request, 'Exam was not created')

    return render(request, 'exams/exam_detail.html', context)

  else:

    # If GET request came from calendar
    if 'is_calendar_form' in request.GET:
      exam_id = request.GET['exam_id']
      exam = Exam.objects.get(id=exam_id)

      context = {
        'exam_id': exam.id,
        'user_id': exam.user_id,
        'title': exam.title,
        'description': exam.description,
        'exam_number': exam.exam_number,
        'predicted_study_hours': exam.predicted_study_hours,
        'predicted_weeks': exam.predicted_weeks,
        'predicted_score': exam.predicted_score,
        'final_study_hours': exam.final_study_hours,
        'final_weeks': exam.final_weeks,
        'final_score': exam.final_score,
        'created_date': exam.created_date,
        'event_id': exam.event_id
      }
      context = json.dumps(context, indent=4, sort_keys=True, default=str)

      return HttpResponse(context)

    if not request.user.is_authenticated:
      messages.error(request, 'Access denied. Must be logged in')
      return redirect('exam_list') #redirect(url path name)

    # If viewing detail of an existing exam, fill the form with its values. if not, show form with blank and default values
    context = {}

    if exam_id > 0:
      exam = get_object_or_404(Exam, pk=exam_id)

      form = ExamForm(initial={
        'exam_id': exam.id,
        'user_id': exam.user_id,
        'title': exam.title,
        'description': exam.description,
        'exam_number': exam.exam_number,
        'predicted_study_hours': exam.predicted_study_hours,
        'predicted_weeks': exam.predicted_weeks,
        'predicted_score': exam.predicted_score,
        'final_study_hours': exam.final_study_hours,
        'final_weeks': exam.final_weeks,
        'final_score': exam.final_score,
        'created_date': exam.created_date,
        'event_id': exam.event_id
      })
      # Get exam notes and events
      # notes = Note.objects.all().filter(exam_id=exam.id,is_hidden=False)
      # events = Event.objects.all().filter(exam_id=exam.id,is_hidden=False)

      context['form'] = form
      # context['notes'] = notes
      # context['events'] = events

    else:
      form = ExamForm(initial={
        'created_date': datetime.date.today()
      })

      context['form'] = form

    return render(request, 'exams/exam_detail.html', context)

# Search for exams 
def search(request):
  queryset_list = Exam.objects.order_by('-created_date')

  # Title
  if 'title' in request.GET:
    title = request.GET['title']
    # Check if empty string
    if title:
      # Search title for anything that matches a keyword
      queryset_list = queryset_list.filter(title__icontains=title)

  context = {
    'exams': queryset_list,
  }

  # Request contains at least one form field, return the form with its field values
  if 'title' in request.GET:
    form = ExamForm(initial={
          'title': request.GET['title'],
          'created_date': request.GET['created_date'],
        })

    search_form_defaults(form)

    context['form'] = form

  # Request does not contain form submission, return empty form
  else:
    form = ExamForm()

    search_form_defaults(form)

    context['form'] = form


  return render(request, 'exams/exam_search.html', context)

# Marks an exam as hidden
def remove(request):
  if request.method == 'POST':
    exam_id = request.POST['exam_id']

    exam = Exam.objects.get(id=exam_id)
    exam.is_hidden = True
    exam.save()

    if 'is_detail' in request.POST:
      return redirect('exam_list')
    else:
      return HttpResponse('')


# Marks are required fields as not required and adds an 'Any' value to the drop down lists
def search_form_defaults(form):
  form.fields['title'].required = False
  form.fields['created_date'].required = False

  # form.fields['event_type'].empty_label = 'Any Type'
