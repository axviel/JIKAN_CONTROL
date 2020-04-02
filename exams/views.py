from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse

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

      # Searches the db for an exam with the id and updates it. if not found, creates a new exam and returns is_created=True
      exam, is_created = Exam.objects.update_or_create(
          id=exam_id,
          defaults={
            'user_id': request.user.id,
            'title': title,
            'description': description,
            'exam_number': exam_number,
            'event': event,
            'course': course,
            'predicted_study_hours': predicted_study_hours,
            'predicted_weeks': predicted_weeks,
            'predicted_score': predicted_score,
            'final_study_hours': final_study_hours,
            'final_weeks': final_weeks,
            'final_score': final_score,
            'created_date': created_date
            },
      )

      # Save in the db
      exam.save()

      # If exam was created via calendar page, return the id
      # if 'is_calendar_form' in request.POST:
      #   context = {
      #     'exam_id': exam.id,
      #     'title': exam.title,
      #     'start_time': exam.start_time.strftime("%H:%M")
      #   }
      #   context = json.dumps(context)
      #   return HttpResponse(context)

      # Create study time events if new or predicted study hours was updated
      generate_study_time_events(exam)

      # UI success message
      messages.success(request, 'Exam created successfully')

      form.fields['event'].queryset = Event.objects.filter(Q(is_hidden=False, event_type_id=4) & ( Q(pk=exam.event.pk) | Q(exam=None) ) ).distinct()

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
        'event': exam.event.pk,
        'course': exam.course.pk,
      })
      # Get exam notes and events
      # notes = Note.objects.all().filter(exam_id=exam.id,is_hidden=False)
      # events = Event.objects.all().filter(exam_id=exam.id,is_hidden=False)

      # Set custom field filtering
      # form.fields['event'].queryset = Event.objects.filter(Q(is_hidden=False, event_type_id=4) & ( Q(pk=exam.event.pk) | Q(exam=None) ) ).distinct()

      # Set custom event field filtering
      form.fields['event'].queryset = Event.objects.filter(Q(is_hidden=False, event_type_id=4) & ( Q(pk=exam.event.pk) | Q(exam=None) ) ).distinct()

      context['form'] = form
      # context['notes'] = notes
      # context['events'] = events

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
def generate_study_time_events(exam):
  # Find the day of the exam
  event = Event.objects.get(pk=exam.event_id)
  event_date = event.start_date

  # Find today
  current_date = datetime.date.today()

  # Get events in between
  # events_in_between = Event.objects.filter(start_date__gt=current_date, start_date__lt=event_date)
  events_in_between = Event.objects.filter(
      Q(is_hidden=False)
      & 
      (
        ( Q(start_date__gte=current_date) & Q(start_date__lt=event_date) ) 
        |
        (~Q(repeat_type=1) 
          & 
          ( Q(end_date__gte=current_date) | Q(end_date=None) ) 
        )
      )
    )

  # Find days between
  # dates_in_between = []
  dates_in_between = {}
  available_hours = {}
  # dates_in_between = OrderedDict()

  other_date = current_date + relativedelta.relativedelta(days=1)
  while (other_date.day != event_date.day) or (other_date.month != event_date.month) or (other_date.year != event_date.year):
    # dates_in_between.append(other_date)
    dates_in_between[f'{other_date.month}/{other_date.day}/{other_date.year}'] = []
    available_hours[f'{other_date.month}/{other_date.day}/{other_date.year}'] = []
    other_date = other_date + relativedelta.relativedelta(days=1)

  # 
  for event in events_in_between:
    repeat_type = event.repeat_type.pk
    start_hour = event.start_time.hour
    end_hour = event.end_time.hour
    start_month = event.start_date.month
    start_day = event.start_date.day
    start_year = event.start_date.year
    start_week_day = event.start_date.weekday()
    end_month = None
    end_day = None
    end_year = None
    if event.end_date != None:
      end_month = event.end_date.month
      end_day = event.end_date.day
      end_year = event.end_date.year

    add_event_hours = False

    for key in dates_in_between:
      # If date is event end_date then break
      if key == f'{end_month}/{end_day}/{end_year}':
        break

      # Start adding the event
      if key == f'{start_month}/{start_day}/{start_year}':
        add_event_hours = True
        # dates_in_between[key].append(event) # testing
        dates_in_between[key].append( (start_hour, end_hour) )

        # If event does not repeat then break
        if repeat_type == 1:
          break
        else:
          continue

      # If event started before our current date
      if event.start_date.date() <= current_date:
        add_event_hours = True

      # If event is stil not being added
      if not add_event_hours:
        continue

      key_date_values = key.split('/')
      key_date = datetime.datetime(int(key_date_values[2]), int(key_date_values[0]), int(key_date_values[1]))

      # If repeats daily, add it
      if add_event_hours and repeat_type == 2:
        # dates_in_between[key].append(event) # testing
        dates_in_between[key].append( (start_hour, end_hour) )
      # If repeats weekly, add it if week day is the same
      elif add_event_hours and repeat_type == 3 and start_week_day == key_date.weekday():
        # dates_in_between[key].append(event) # testing
        dates_in_between[key].append( (start_hour, end_hour) )
      # If repeats monthly, add if day is the same
      elif add_event_hours and repeat_type == 4 and start_day == key_date.day:
        # dates_in_between[key].append(event) # testing
        dates_in_between[key].append( (start_hour, end_hour) )
      # If repeats yearly, add if day, month are the same
      elif add_event_hours and repeat_type == 5 and start_month == key_date.month and start_day == key_date.day:
        # dates_in_between[key].append(event) # testing
        dates_in_between[key].append( (start_hour, end_hour) )

  # Contains the free time hours of the days in between
  total_study_hours = exam.predicted_study_hours * 4 # 4 weeks worth of hours
  total_study_hours_old = 0
  study_hour_added = False

  study_events = {}
  study_event_exists = False

  # Hide existing exam_study 
  # ExamStudy.objects.filter(exam=exam.id).update(is_hidden=True)
  ExamStudy.objects.filter(exam=exam.id).delete()
  # Event.objects.filter(pk=exam.event.pk).update(is_hidden=True)
  
  while total_study_hours > 0 and total_study_hours_old != total_study_hours:
    total_study_hours_old = total_study_hours
    for key in dates_in_between:
      key_date_values = key.split('/')

      study_hour = 7

      study_event = Event()

      if available_hours[key] != []:
        study_hour = available_hours[key][-1] + 1
        study_event = study_events[key]
        study_event_exists = True

      if study_hour >= 24:
        continue

      if dates_in_between[key] == []:
        study_hour_added = True
        if study_event_exists:
          study_event.end_time = datetime.time(study_hour, 59)
        else:
          # Add event data
          study_event.event_type_id = 3
          study_event.repeat_type_id = 1
          study_event.title = f'{exam.title} study time'
          study_event.description = f'{exam.title} study time based on predicted score'
          study_event.start_time = datetime.time(study_hour, 0)
          study_event.end_time = datetime.time(study_hour, 59)
          study_event.start_date = datetime.datetime(int(key_date_values[2]), int(key_date_values[0]), int(key_date_values[1]))
          study_event.user_id = exam.user_id

          exam_study = ExamStudy()
          exam_study.exam_id = exam.pk
          exam_study.is_hidden = False
      else:
        for event_hours in dates_in_between[key]:
          # If there's an event hour that conflicts with study_hour, change study hour to hour after event
          if study_hour >= event_hours[0] and study_hour <= event_hours[1] :
            study_hour = event_hours[1] + 1
            study_hour_added = True
          else:
            study_hour_added = True

          if study_hour_added:
            if study_event_exists:
              study_event.end_time = datetime.time(study_hour, 59)
            else:
              study_event.event_type_id = 3
              study_event.repeat_type_id = 1
              study_event.title = f'{exam.title} study time'
              study_event.description = f'{exam.title} study time based on predicted score'
              study_event.start_time = datetime.time(study_hour, 0)
              study_event.end_time = datetime.time(study_hour, 59)
              study_event.start_date = datetime.datetime(int(key_date_values[2]), int(key_date_values[0]), int(key_date_values[1]))
              study_event.user_id = exam.user_id

              exam_study = ExamStudy()
              exam_study.exam_id = exam.pk
              exam_study.is_hidden = False

      if study_hour > 24:
        study_hour = 24
        continue

      if study_hour_added:
        available_hours[key].append(study_hour)
        total_study_hours -= 1
        study_event.save()

        if not study_event_exists:
          study_events[key] = study_event
          exam_study.event_id = study_event.pk
          exam_study.save()

      if total_study_hours == 0:
        break

      study_hour_added = False
      study_event_exists = False

  x = 0

  # Assign study events to those hours and an ExamStudy relation 
  # for key in available_hours:




  return 0

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