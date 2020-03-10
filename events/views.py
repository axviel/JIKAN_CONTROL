from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse

from .models import Event, EventType, RepeatType
from .forms import EventForm

import datetime
import json

# Returns the list page with all events
def index(request):
  # Fetch events from db
  events = Event.objects.order_by('-start_date').filter(is_hidden=False)

  # Pagination
  paginator = Paginator(events, 10)
  page = request.GET.get('page')
  paged_events = paginator.get_page(page)

  # Data that is passed to the template
  context = {
    'events': paged_events,
  }

  # Renders the template with the data that can be accesed
  return render(request, 'events/event_list.html', context)

# Returns the detail info of an Event. Also used to create and update events
def event(request, event_id=0):
  if request.method == "POST":
    # Kick user if not logged in
    if not request.user.is_authenticated:
      messages.error(request, 'Unauthorized. Must be logged in')
      return redirect('event_list')

    # Get the POST form
    form = EventForm(request.POST)

    if form.is_valid():
      event_id = form.cleaned_data['event_id']
      title = form.cleaned_data['title']
      description = form.cleaned_data['description']
      start_time = form.cleaned_data['start_time']
      end_time = form.cleaned_data['end_time']
      start_date = form.cleaned_data['start_date']
      event_type_id = request.POST['event_type']
      repeat_type_id = request.POST['repeat_type']

      event_type = get_object_or_404(EventType, pk=event_type_id)
      repeat_type = get_object_or_404(RepeatType, pk=repeat_type_id)

      # Searches the db for an event with the id and updates it. if not found, creates a new event and returns is_created=True
      event, is_created = Event.objects.update_or_create(
          id=event_id,
          defaults={
            'event_type': event_type,
            'repeat_type': repeat_type,
            'title': title,
            'description': description,
            'start_time': start_time,
            'end_time': end_time,
            'start_date': start_date,
            'user_id': request.user.id,
            },
      )

      # Save in the db
      event.save()

      # If event was created via calendar page, return the id
      if 'is_calendar_form' in request.POST:
        context = {
          'event_id': event.id,
          'title': event.title
        }
        context = json.dumps(context)
        return HttpResponse(context)

      # UI success message
      messages.success(request, 'Event created successfully')

      # If it was updated return the page and form
      if not is_created:
        context = {
          'form': form
        }
        return render(request, 'events/event_detail.html', context)

      # If it was created, redirect to url with id
      return redirect('event_detail', event_id=event.id) #redirect(url path name, id specified in the path)

    # Form was invalid, so return it
    context = {
      'form': form
    }

    # UI error message
    messages.error(request, 'Event was not created')

    return render(request, 'events/event_detail.html', context)

  else:

    # If GET request came from calendar
    if 'is_calendar_form' in request.GET:
      event_id = request.GET['event_id']
      event = Event.objects.get(id=event_id)

      context = {
        'event_id': event.id,
        'title': event.title,
        'description': event.description,
        'event_type': event.event_type.pk,
        'repeat_type': event.repeat_type.pk,
        'start_date': event.start_date,
        'start_time': event.start_time,
        'end_time': event.end_time
      }
      context = json.dumps(context, indent=4, sort_keys=True, default=str)

      return HttpResponse(context)

    if not request.user.is_authenticated:
      messages.error(request, 'Access denied. Must be logged in')
      return redirect('event_list') #redirect(url path name)

    # If viewing detail of an existing event, fill the form with its values. if not, show form with blank and default values
    context = {}

    if event_id > 0:
      event = get_object_or_404(Event, pk=event_id)

      form = EventForm(initial={
        'event_id': event.id,
        'title': event.title,
        'description': event.description,
        'event_type': event.event_type.pk,
        'repeat_type': event.repeat_type.pk,
        'start_date': event.start_date,
        'start_time': event.start_time,
        'end_time': event.end_time
      })

      context['form'] = form
    else:
      form = EventForm(initial={
        'start_date': datetime.date.today()
      })

      context['form'] = form

    return render(request, 'events/event_detail.html', context)

# Search for events 
def search(request):
  queryset_list = Event.objects.order_by('-start_date')

  # Title
  if 'title' in request.GET:
    title = request.GET['title']
    # Check if empty string
    if title:
      # Search title for anything that matches a keyword
      queryset_list = queryset_list.filter(title__icontains=title)

  # Event Type
  if 'event_type' in request.GET:
    event_type = request.GET['event_type']
    if event_type:
      queryset_list = queryset_list.filter(event_type__exact=event_type)

  # Repeat Type
  if 'repeat_type' in request.GET:
    repeat_type = request.GET['repeat_type']
    if repeat_type:
      queryset_list = queryset_list.filter(repeat_type__exact=repeat_type)

  # Start Date
  if 'start_date' in request.GET:
    start_date = request.GET['start_date']
    if start_date:
      queryset_list = queryset_list.filter(start_date__exact=start_date)

  # End Date
  if 'end_date' in request.GET:
    end_date = request.GET['end_date']
    if end_date:
      queryset_list = queryset_list.filter(end_date__exact=end_date)

  # Start Time
  if 'start_time' in request.GET:
    start_time = request.GET['start_time']
    if start_time:
      queryset_list = queryset_list.filter(start_time__lte=start_time)

  # End Time
  if 'end_time' in request.GET:
    end_time = request.GET['end_time']
    if end_time:
      queryset_list = queryset_list.filter(end_time__lte=end_time)

  context = {
    'events': queryset_list,
  }

  # Request contains at least one form field, return the form with its field values
  if 'title' in request.GET:
    form = EventForm(initial={
          'title': request.GET['title'],
          'event_type': request.GET['event_type'],
          'repeat_type': request.GET['repeat_type'],
          'start_date': request.GET['start_date'],
          'end_date': request.GET['end_date'],
          'start_time': request.GET['start_time'],
          'end_time': request.GET['end_time']
        })

    search_form_defaults(form)

    context['form'] = form

  # Request does not contain form submission, return empty form
  else:
    form = EventForm()

    search_form_defaults(form)

    context['form'] = form


  return render(request, 'events/event_search.html', context)

# Marks an event as hidden
def remove(request):
  if request.method == 'POST':
    event_id = request.POST['id']

    event = Event.objects.get(id=event_id)
    event.is_hidden = True
    event.save()

    return HttpResponse('')

# Marks are required fields as not required and adds an 'Any' value to the drop down lists
def search_form_defaults(form):
  form.fields['title'].required = False
  form.fields['event_type'].required = False
  form.fields['repeat_type'].required = False
  form.fields['start_date'].required = False
  form.fields['end_date'].required = False
  form.fields['start_time'].required = False
  form.fields['end_time'].required = False

  form.fields['event_type'].empty_label = 'Any Type'
  form.fields['repeat_type'].empty_label = 'Any Type'