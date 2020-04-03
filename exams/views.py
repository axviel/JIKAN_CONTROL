from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db import connection

from django.db.models import Q

from .models import Exam
from .forms import ExamForm

from events.models import Event
from notes.models import Note
from exams.models import Exam
from courses.models import Course
from examstudy.models import ExamStudy

import datetime
from dateutil import relativedelta
import json
from collections import OrderedDict 

from ml import ml

def index(request):
  # Fetch exams from db
  exams = Exam.objects.order_by('-created_date').filter(is_hidden=False, user_id=request.user.id)

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
def exam(request, exam_id=0, event_id=0):
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
      event_id = request.POST['event']
      course_id = request.POST['course']
      predicted_study_hours = form.cleaned_data['predicted_study_hours']
      predicted_weeks = form.cleaned_data['predicted_weeks']
      predicted_score = form.cleaned_data['predicted_score']
      final_study_hours = form.cleaned_data['final_study_hours']
      final_weeks = form.cleaned_data['final_weeks']
      final_score = form.cleaned_data['final_score']
      created_date = datetime.date.today()

      event = get_object_or_404(Event, pk=event_id)
      course = get_object_or_404(Course, pk=course_id)

      # Used to determine if study events will be generated
      prev_predicted_study_hours = 0
      # Used to determine the return response
      is_new = False
      
      # Get exam
      exam = Exam.objects.filter(id=exam_id)

      # If exam doesn't exist, create a new one
      if len(exam) == 0:
        exam = Exam()
        is_new = True
      # If exists, save previous study hours
      else:
        exam = exam[0]
        prev_predicted_study_hours = exam.predicted_study_hours

      # Add exam info
      exam.title = title
      exam.description = description
      exam.exam_number = exam_number
      exam.event = event
      exam.course = course
      exam.predicted_study_hours = predicted_study_hours
      exam.predicted_weeks = predicted_weeks
      exam.predicted_score = predicted_score
      exam.final_study_hours = final_study_hours
      exam.final_weeks = final_weeks
      exam.final_score = final_score
      exam.created_date = created_date
      exam.user_id = request.user.id

      # Save in the db
      exam.save()

      # Create study time events if new or predicted study hours was updated
      # TODO Handle remaining_hours > 0
      remaining_hours = 0
      if prev_predicted_study_hours == 0 or predicted_study_hours != prev_predicted_study_hours:
        remaining_hours = generate_study_time_events(exam, event)

      # UI success message
      messages.success(request, 'Exam saved successfully')

      form.fields['event'].queryset = Event.objects.filter(Q(is_hidden=False, event_type_id=4) & ( Q(pk=exam.event.pk) | Q(exam=None) ) ).distinct()

      # If it was updated return the page and form
      if not is_new:
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
        'event': exam.event.pk,
        'course': exam.course.pk,
      })

      # Set custom event field filtering
      form.fields['event'].queryset = Event.objects.filter(Q(is_hidden=False, event_type_id=4) & ( Q(pk=exam.event.pk) | Q(exam=None) ) ).distinct()

      context['form'] = form

    elif event_id > 0:
      form = ExamForm(initial={
        'created_date': datetime.date.today(),
        'exam_number': 1,
        'predicted_weeks': 4,
        'final_weeks': 4,
        'event': event_id
      })

      # Set custom event field filtering
      form.fields['event'].queryset = Event.objects.filter(Q(is_hidden=False, event_type_id=4) & Q(exam=None) ).distinct()

      context['form'] = form

    else:
      form = ExamForm(initial={
        'created_date': datetime.date.today(),
        'exam_number': 1,
        'predicted_weeks': 4,
        'final_weeks': 4,
      })

      # Set custom event field filtering
      form.fields['event'].queryset = Event.objects.filter(Q(is_hidden=False, event_type_id=4) & Q(exam=None) ).distinct()

      context['form'] = form

  
    return render(request, 'exams/exam_detail.html', context)

# When there is a change in predicted study hours, generate the study time events
def generate_study_time_events(exam, event):
  # Find the day of the exam
  event_date = event.start_date
  # Find today
  current_date = datetime.date.today()
  remaining_hours = exam.predicted_study_hours * 4

  # Create parameters for generate_study_events SQL function
  params = []
  params.append(current_date + relativedelta.relativedelta(days=1)) # start_date
  params.append(event_date - relativedelta.relativedelta(days=1)) # end_date
  params.append(datetime.time(7,0,0)) # first_hour
  params.append(datetime.time(0,0,0)) # last_hour
  params.append(remaining_hours) # remaining_hours
  params.append(exam.pk) # exam_id
  params.append(exam.title) # exam_title
  params.append(exam.user_id) # user_id

  with connection.cursor() as cursor:
    # FIXME
    # Update Study events and ExamStudy records
    cursor.execute("CALL update_study_events(%s)", [exam.pk])

    # Generate study events
    cursor.execute("SELECT * FROM generate_study_events(%s, %s, %s, %s, %s, %s, %s, %s)", params)
    remaining_hours = cursor.fetchone()[0]

  return remaining_hours

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

# Gets the exam id that's linked to a event
def get_exam_id(request):

  event_id = request.GET['event_id']
  # exam = get_object_or_404(Exam, event_id=event_id, is_hidden=False)
  exam = Exam.objects.filter(event_id=event_id, is_hidden=False).first()

  context = {}

  if exam == None:
    context['exam_id'] = None
  else:
    context['exam_id'] = exam.id

  context = json.dumps(context)

  return HttpResponse(context)

# Marks are required fields as not required and adds an 'Any' value to the drop down lists
def search_form_defaults(form):
  form.fields['title'].required = False
  form.fields['created_date'].required = False

  # form.fields['event_type'].empty_label = 'Any Type'

# Returns the predicted exam score
def predict_score(request):

  study_hours = int(request.GET['predicted_study_hours'])
  exam_number = int(request.GET['exam_number'])
  course_id = int(request.GET['course_id'])

  context = {
    'score': int(ml.get_exam_prediction(exam_number, course_id, study_hours))
  }

  context = json.dumps(context)

  return HttpResponse(context)

# Returns the predicted study hours
def predict_study_hours(request):

  predicted_score = int(request.GET['predicted_score'])
  exam_number = int(request.GET['exam_number'])
  course_id = int(request.GET['course_id'])

  context = {
    'hours': int(ml.get_hours_prediction(exam_number, course_id, predicted_score))
  }
  
  context = json.dumps(context)

  return HttpResponse(context)