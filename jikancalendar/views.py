from django.shortcuts import render

from events.models import Event
from events.views import remove as event_remove
from events.forms import EventForm

import datetime
import json
from dateutil import relativedelta
from calendar import monthrange

def index(request):

  current_date = datetime.date.today()
  start_date = current_date.replace(day=1) - relativedelta.relativedelta(months=6)
  month_days = monthrange(start_date.year + 1, start_date.month)[1]
  end_date = start_date.replace(day=month_days, month=start_date.month, year=(start_date.year + 1))

  events = Event.objects.raw('SELECT * FROM get_events_in_range(%s, %s, %s)', [start_date, end_date,request.user.id])

  events_data = {}

  for event in events:
    key = event.start_date.strftime("%m/%d/%Y")

    end_date = event.end_date
    if end_date != None:
      end_date = end_date.strftime("%m/%d/%Y")

    event_data = {
        'event_id': event.id,
        'title': event.title,
        'event_type': event.event_type.pk,
        'repeat_type': event.repeat_type.pk,
        'start_date': key,
        'end_date': end_date,
        'start_time': event.start_time.strftime("%H:%M"), # Keep only hour and minutes
        'end_time': event.end_time.strftime("%H:%M"),
        'is_completed': event.is_completed
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
  context['form'].fields['end_date'].widget.attrs['disabled'] = True

  return render(request, 'calendar/calendar.html', context)
