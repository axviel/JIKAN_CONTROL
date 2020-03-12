from django.shortcuts import render

from events.models import Event
from events.views import remove as event_remove
from events.forms import EventForm

from datetime import datetime

def index(request):

  events = Event.objects.all().filter(is_hidden=False)
  events_data = {}

  for event in events:
    key = event.start_date.strftime("%d/%m/%Y")

    event_data = {
        'event_id': event.id,
        'title': event.title,
        'start_time': event.start_time.strftime("%H:%M") # Keep only hour and minutes
      }

    if key in events_data:
      events_data[key].append(event_data)
    else:
      events_data[key] = [event_data]

  context = {
    'events': events_data,
    'form': EventForm()
  }

  # Disable date field
  context['form'].fields['start_date'].widget.attrs['disabled'] = True

  return render(request, 'calendar/calendar.html', context)
