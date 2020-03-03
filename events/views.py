from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Event

import datetime

def index(request):
  # Fetch events from db
  # events = Event.objects.all()
  events = Event.objects.order_by('-start_date').filter(is_hidden=False)

  # Pagination
  paginator = Paginator(events, 5)
  page = request.GET.get('page')
  paged_events = paginator.get_page(page)

  # Data that is passed to the template
  context = {
    # 'events': events
    'events': paged_events
  }

  return render(request, 'events/event_list.html', context)

def event(request, event_id):
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
  else:
    return render(request, 'events/event_detail.html')

def search(request):
  return render(request, 'events/event_search.html')