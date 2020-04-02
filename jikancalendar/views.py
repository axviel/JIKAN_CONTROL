from django.shortcuts import render
from django.db import connection

from events.models import Event
from events.views import remove as event_remove
from events.forms import EventForm

import datetime
import json
from dateutil import relativedelta
from calendar import monthrange

def index(request):

  events = Event.objects.all().filter(is_hidden=False, user_id=request.user.id)
  events_data = {}

  for event in events:
    # key = event.start_date.strftime("%d/%m/%Y")
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
        'is_completed': (event.end_date != None)
      }

    if key in events_data:
      events_data[key].append(event_data)
    else:
      events_data[key] = [event_data]

  # Get events of an entire year
  current_date = datetime.date.today()
  start_date = current_date.replace(day=1) - relativedelta.relativedelta(months=6)
  month_days = monthrange(start_date.year + 1, start_date.month)[1]
  end_date = start_date.replace(day=month_days, month=start_date.month, year=(start_date.year + 1))

  db_events = query_db("select * from get_events_in_range(%s, %s, %s)", (start_date, end_date,request.user.id))
  # db_events = json.dumps(db_events, indent=4, sort_keys=True, default=str)

  context = {
    'events': events_data,
    'form': EventForm(),
    'events_db': db_events
  }

  # Disable date field
  context['form'].fields['start_date'].widget.attrs['disabled'] = True
  context['form'].fields['end_date'].widget.attrs['disabled'] = True

  return render(request, 'calendar/calendar.html', context)


def query_db(query, args=(), one=False):
  with connection.cursor() as cursor:
    cursor.execute(query, args)
    r = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]
    return (r[0] if r else None) if one else r
