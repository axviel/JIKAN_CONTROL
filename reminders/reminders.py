from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from webpush import send_user_notification
from django.core import serializers
from events.models import Event
from queue import PriorityQueue

import multiprocessing 
import threading
import time
import datetime

all_processes = []

def repeats(time, repeat):
  if repeat == 1:
    return None
  elif repeat == 2:
    return time + datetime.timedelta(days=1)
  elif repeat == 3:
    return time + datetime.timedelta(weeks=1)
  elif repeat == 4:
    new_year = time.year
    new_month = time.month + 1
    if new_month > 12:
      new_year += 1
      new_month -= 12
    try:
        return time.replace(year=new_year, month=new_month)
    except ValueError:
        return time.replace(year=new_year, month=new_month + 1)
  elif repeat == 5:
    try:
      return time.replace(year = time.year + 1)
    except ValueError:
      new_year = time.year + 4
      return time.replace(year = new_year)


def next_reminder(time, event):
  current_time = datetime.datetime.now()
  while time < current_time:
    time = repeats(time, event['repeat_type'])
  time = time - current_time
  return time.total_seconds()


def reminder(uid):
  events = Event.objects.all().filter(is_hidden=False, user_id=uid)
  events = serializers.serialize('python', events)
  for eventModel in events:
    eventModel['fields']['id'] = eventModel['pk']
    eventModel['fields']['start_time'] = eventModel['fields']['start_time'].strftime("%H:%M")
    eventModel['fields']['end_time'] = eventModel['fields']['end_time'].strftime("%H:%M")

    eventModel['fields']['start_date'] = eventModel['fields']['start_date'].strftime("%m/%d/%Y")
    if eventModel['fields']['end_date'] != None:
      eventModel['fields']['end_date'] = eventModel['fields']['end_date'].strftime("%m/%d/%Y")
  
  datetimeFormat = '%m/%d/%Y %H:%M:%S.%f'
  reminders = PriorityQueue()

  for e in events:
    event = e['fields']
    if not event['is_hidden'] and not event['is_completed']:
      start = event['start_date'] + ' ' + event['start_time'] + ':0.0'
      current_time = datetime.datetime.now()
      if event['repeat_type'] > 1:
        edate = event['end_date']
        if edate == None:
          event_t = datetime.datetime.strptime(start, datetimeFormat)
          secs = next_reminder(event_t, event)
          rem = (secs, event['title'], event['description'], event['repeat_type'], None)
          reminders.put(rem)
        else:
          end = edate + ' ' + event['start_time'] + ':0.0'
          end = datetime.datetime.strptime(end, datetimeFormat)
          if end > current_time:
            event_t = datetime.datetime.strptime(start, datetimeFormat)
            secs = next_reminder(event_t, event)
            rem = (secs, event['title'], event['description'], event['repeat_type'], edate)
            reminders.put(rem)
      elif datetime.datetime.strptime(start, datetimeFormat) > current_time:
        event_t = datetime.datetime.strptime(start, datetimeFormat) - current_time
        rem = (event_t.total_seconds(), event['title'], event['description'], 1)
        reminders.put(rem)
  
  return reminders


def multithread(uid):
  reminders = reminder(uid)
  user_model = get_user_model()
  user = get_object_or_404(user_model, pk=uid)

  elapsed_time = 0
  while not reminders.empty():
    rem = reminders.get()
    timer = rem[0] - elapsed_time
    process = multiprocessing.Process(target=time.sleep, args=(timer,), name="%s" % (uid), )
    all_processes.append(process)
    process.start()
    process.join()
    if process.exitcode != 0:
      break
    elapsed_time = elapsed_time + timer

    currt = datetime.datetime.now()
    next_r = repeats(currt, rem[3])
    if next_r != None:
      next_r.replace(second=0, microsecond=0)
      if rem[4] != None:
        if next_r <= rem[4]:
          total = next_r - currt
          result = total.total_seconds() + elapsed_time
          reminders.put((result, rem[1], rem[2], rem[3], rem[4]))
      else:
        total = next_r - currt
        result = total.total_seconds() + elapsed_time
        reminders.put((result, rem[1], rem[2], rem[3], rem[4]))

    payload = {"head": "Event started: " + rem[1], "body": rem[2]}
    send_user_notification(user=user, payload=payload, ttl=1000)


def main(uid):
  pcs = all_processes
  remove = None
  for p in pcs:
    if p.name == "%s" % uid:
      p.kill()
      remove = p
      break
  if remove != None:
    all_processes.remove(remove)
  t = threading.Thread(target=multithread, args=(uid,), name="Reminder-%s" % (uid))
  t.start()
