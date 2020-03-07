from django.shortcuts import render

from events.models import Event
from events.views import remove as event_remove

from datetime import datetime

def index(request):

  events = Event.objects.all().filter(is_hidden=False)
  events_data = {}

  for event in events:
    key = event.start_date.strftime("%d/%m/%Y")
    # key = '17/1/2020'
    if key in events_data:
      events_data[key].append(event.title)
    else:
      events_data[key] = [event.title]

  context = {
    'events': events_data
  }

  return render(request, 'calendar/calendar.html', context)
