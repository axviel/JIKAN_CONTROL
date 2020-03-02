from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Event

import datetime

def events(request):
  return render(request, 'events/list.html')

def detail(request):
  if request.method == "POST":
    user_id = request.POST['user_id']
    title = request.POST['title']
    description = request.POST['description']
    event_type = request.POST['event-type']
    start_date = request.POST.get('event-date')
    start_time = request.POST.get('start-time')
    end_time = request.POST.get('end-time')
    repeat_type = request.POST['repeat-type']

    event = Event(event_type_id=event_type, repeat_type_id=repeat_type, title=title, description=description,start_time=start_time, end_time=end_time, start_date=start_date, user_id=user_id)

    event.save()

    messages.success(request, 'Event created successfully')

    return redirect('events')