from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib import messages

from events.models import Event
from events.forms import EventForm

# Gets all of the user's events and the Event Form
def index(request):
  if not request.user.is_authenticated:
      messages.error(request, 'Unauthorized. Must be logged in')
      return redirect('login')

  events = Event.objects.all().filter(is_hidden=False, user_id=request.user.id)
  events_data = []
  json_events = serializers.serialize('python', events)
  for eventModel in json_events:
    eventModel['fields']['id'] = eventModel['pk']
    eventModel['fields']['start_time'] = eventModel['fields']['start_time'].strftime("%H:%M")
    eventModel['fields']['end_time'] = eventModel['fields']['end_time'].strftime("%H:%M")

    eventModel['fields']['start_date'] = eventModel['fields']['start_date'].strftime("%m/%d/%Y")
    if eventModel['fields']['end_date'] != None:
      eventModel['fields']['end_date'] = eventModel['fields']['end_date'].strftime("%m/%d/%Y")

    events_data.append(eventModel['fields'])

  context = {
    'events': events_data,
    'form': EventForm(),
  }

  # Disable date field
  context['form'].fields['start_date'].widget.attrs['disabled'] = True
  context['form'].fields['end_date'].widget.attrs['disabled'] = True

  return render(request, 'calendar/calendar.html', context)
