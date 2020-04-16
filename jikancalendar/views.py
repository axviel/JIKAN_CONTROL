from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib import messages

from events.models import Event
from events.forms import EventForm

import time
import datetime

from asgiref.sync import async_to_sync

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
  reminder(json_events)
  return render(request, 'calendar/calendar.html', context)


def next_reminder(time, repeat):
  if repeat == 2:
    return time + datetime.timedelta(days=1)
  elif repeat == 3:
    return time + datetime.timedelta(days=7)
  elif repeat == 4:
    return time + datetime.timedelta(days=30)
  elif repeat == 5:
    return time + datetime.timedelta(days=365)


def reminder(events):
  datetimeFormat = '%m/%d/%Y %H:%M:%S.%f'
  current_time = datetime.datetime.now()
  reminders = []
  for e in events:
    event = e['fields']
    if event['is_hidden'] == False and event['is_completed'] == False:
      start = event['start_date'] + ' ' + event['start_time'] + ':0.0'
      if event['repeat_type'] > 1:
        edate = event['end_date']
        etime = event['end_time']
        if edate == None or etime == None:
          time = datetime.datetime.strptime(start, datetimeFormat)
          while time < current_time:
            time = next_reminder(time, event['repeat_type'])
          time = time - current_time
          rem = (time.total_seconds(), event['title'], event['repeat_type'], None)
          reminders.append(rem)
        else:
          end = event['end_date'] + ' ' + event['end_time'] + ':0.0'
          if datetime.datetime.strptime(end, datetimeFormat) > current_time:
            time = datetime.datetime.strptime(start, datetimeFormat)
            while time < current_time:
              time = next_reminder(time, event['repeat_type'])
            time = time - current_time
            rem = (time.total_seconds(), event['title'], event['repeat_type'], None)
            reminders.append(rem)
      elif datetime.datetime.strptime(start, datetimeFormat) > current_time:
        time = datetime.datetime.strptime(start, datetimeFormat) - current_time
        rem = (time.total_seconds(), event['title'], 1)
        reminders.append(rem)

  local_time = 70
  local_time = local_time * 60
  # time.sleep(local_time)
