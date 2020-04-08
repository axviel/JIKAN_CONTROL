from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse

from .models import Course
from .forms import CourseForm
import datetime
import json

# Returns the list page with all courses
def index(request):
  if not request.user.is_authenticated:
    messages.error(request, 'Unauthorized. Must be logged in')
    return redirect('login')

  # Fetch courses from db
  courses = Course.objects.order_by('title').filter(is_hidden=False, user_id=request.user.id)

  # Pagination
  paginator = Paginator(courses, 10)
  page = request.GET.get('page')
  paged_courses = paginator.get_page(page)

  # Data that is passed to the template
  context = {
    'courses': paged_courses,
  }

  # Renders the template with the data that can be accesed
  return render(request, 'courses/course_list.html', context)

# Returns the detail info of a course. Also used to create and update courses
def course(request, course_id=0):
  if request.method == "POST":
    # Kick user if not logged in
    if not request.user.is_authenticated:
      messages.error(request, 'Unauthorized. Must be logged in')
      return redirect('login')

    # Get the POST form
    form = CourseForm(request.POST)

    if form.is_valid():
      course_id = form.cleaned_data['course_id']
      title = form.cleaned_data['title']
      description = form.cleaned_data['description']

      # Searches the db for a course with the id and updates it. if not found, creates a new course and returns is_created=True
      course, is_created = Course.objects.update_or_create(
          id=course_id,
          defaults={
            'title': title,
            'description': description,
	          'user_id': request.user.id
            },
      )

      # Save in the db
      course.save()

      # If event was created via calendar page, return the id
      if 'is_calendar_form' in request.POST:

        context = {
          'id': course.id,
          'title': course.title,
          'description': course.description,
	        'user_id': request.user.id
        }
        context = json.dumps(context)
        return HttpResponse(context)

      # UI success message
      messages.success(request, 'Course created successfully')

      # If it was updated return the page and form
      if not is_created:
        context = {
          'form': form
        }
        return render(request, 'courses/course_detail.html', context)

      # If it was created, redirect to url with id
      return redirect('course_detail', course_id=course.id) #redirect(url path name, id specified in the path)

    # Form was invalid, so return it
    context = {
      'form': form
    }

    # UI error message
    messages.error(request, 'Course was not created')

    return render(request, 'courses/course_detail.html', context)

  else:
    if not request.user.is_authenticated:
      messages.error(request, 'Unauthorized. Must be logged in')
      return redirect('login')

 # If viewing detail of an existing course, fill the form with its values. if not, show form with blank and default values
    context = {}

    if course_id > 0:
      course = get_object_or_404(Course, pk=course_id)

      form = CourseForm(initial={
        'course_id': course.id,
        'title': course.title,
        'description': course.description
      })
      # Get event notes and exams
      courses = Course.objects.all().filter(title=course.title,is_hidden=False)

      context['form'] = form
      context['courses'] = courses

    else:
      form = CourseForm(initial={
      })

      context['form'] = form

    return render(request, 'courses/course_detail.html', context)

# Search for courses 
def search(request):
  if not request.user.is_authenticated:
      messages.error(request, 'Unauthorized. Must be logged in')
      return redirect('login')

  queryset_list = Course.objects.order_by('title').filter(is_hidden=False, user_id=request.user.id)

  # Title
  if 'title' in request.GET:
    title = request.GET['title']
    # Check if empty string
    if title:
      # Search title for anything that matches a keyword
      queryset_list = queryset_list.filter(title__icontains=title)

  context = {
    'courses': queryset_list,
  }

  # Request contains at least one form field, return the form with its field values
  if 'title' in request.GET:
    form = CourseForm(initial={
          'title': request.GET['title']
        })

    search_form_defaults(form)

    context['form'] = form

  # Request does not contain form submission, return empty form
  else:
    form = CourseForm()

    search_form_defaults(form)

    context['form'] = form


  return render(request, 'courses/course_search.html', context)

# Marks a course as hidden
def remove(request):
  if request.method == 'POST':
    if not request.user.is_authenticated:
      messages.error(request, 'Unauthorized. Must be logged in')
      return redirect('login')

    course_id = request.POST['course_id']

    course = Course.objects.get(id=course_id)
    course.is_hidden = True
    course.save()

    if 'is_detail' in request.POST:
      return redirect('course_list')
    else:
      return HttpResponse('')


# Marks are required fields as not required and adds an 'Any' value to the drop down lists
def search_form_defaults(form):
  form.fields['title'].required = False
