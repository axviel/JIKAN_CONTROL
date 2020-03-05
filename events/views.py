from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Event, EventType, RepeatType
from .forms import EventForm

import datetime

# Returns the list page with all events
def index(request):
  # Fetch events from db
  events = Event.objects.order_by('-start_date').filter(is_hidden=False)

  # Pagination
  paginator = Paginator(events, 5)
  page = request.GET.get('page')
  paged_events = paginator.get_page(page)

  # Data that is passed to the template
  context = {
    'events': paged_events
  }

  # Renders the template with the data that can be accesed
  return render(request, 'events/event_list.html', context)

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

# todo Search for events 
def search(request):
  return render(request, 'events/event_search.html')