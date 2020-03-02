from django.shortcuts import render

def calendar(request):
  return render(request, 'calendar/calendar.html')
