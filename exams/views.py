from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Exam
from .forms import ExamForm

import datetime

def index(request):
  # Fetch exams from db
  exams = Exam.objects.order_by('-created_date').filter(is_hidden=False)

  # Pagination
  paginator = Paginator(exams, 5)
  page = request.GET.get('page')
  paged_exams = paginator.get_page(page)

  # Data that is passed to the template
  context = {
    'exams': paged_exams
  }

  return render(request, 'exams/exam_list.html', context)

# Returns the detail info of an Exam. Also used to create and update exams
def exam(request, exam_id=0):
  if request.method == "POST":
    # Kick user if not logged in
    if not request.user.is_authenticated:
      messages.error(request, 'Unauthorized. Must be logged in')
      return redirect('exam_list')

    # Get the POST form
    form = ExamForm(request.POST)

    if form.is_valid():
      exam_id = form.cleaned_data['exam_id']
      title = form.cleaned_data['title']
      description = form.cleaned_data['description']
      event_id = 0
      predicted_study_hours = 0
      predicted_weeks = 0
      predicted_score = 0
      final_study_hours = 0
      final_weeks = 0
      final_score = 0
      created_date = datetime.date.today()
      # start_time = form.cleaned_data['start_time']
      # end_time = form.cleaned_data['end_time']
      # start_date = form.cleaned_data['start_date']
      # event_type_id = request.POST['event_type']
      # repeat_type_id = request.POST['repeat_type']

      # event_type = get_object_or_404(EventType, pk=event_type_id)
      # repeat_type = get_object_or_404(RepeatType, pk=repeat_type_id)

      # Searches the db for an exam with the id and updates it. if not found, creates a new exam and returns is_created=True
      exam, is_created = Exam.objects.update_or_create(
          id=exam_id,
          defaults={
            # 'event_type': event_type,
            # 'repeat_type': repeat_type,
            # 'start_time': start_time,
            # 'end_time': end_time,
            # 'start_date': start_date,
            'user_id': request.user.id,
            'title': title,
            'description': description,
            'predicted_study_hours': predicted_study_hours,
            'predicted_weeks': predicted_weeks,
            'predicted_score': predicted_score,
            'final_study_hours': final_study_hours,
            'final_weeks': final_weeks,
            'final_score': final_score,
            'created_date': created_date,
            'event_id': event_id,
            },
      )

      # Save in the db
      exam.save()

      # UI success message
      messages.success(request, 'Exam created successfully')

      # If it was updated return the page and form
      if not is_created:
        context = {
          'form': form
        }
        return render(request, 'exams/exam_detail.html', context)

      # If it was created, redirect to url with id
      return redirect('exam_detail', exam_id=exam.id) #redirect(url path name, id specified in the path)

    # Form was invalid, so return it
    context = {
      'form': form
    }

    # UI error message
    messages.error(request, 'Exam was not created')

    return render(request, 'exams/exam_detail.html', context)

  else:
    if not request.user.is_authenticated:
      messages.error(request, 'Access denied. Must be logged in')
      return redirect('exam_list') #redirect(url path name)

    # If viewing detail of an existing exam, fill the form with its values. if not, show form with blank and default values
    context = {}

    if exam_id > 0:
      exam = get_object_or_404(Exam, pk=exam_id)
      form = ExamForm(initial={
        'exam_id': exam.id,
        'title': exam.title,
        'description': exam.description,
        # 'event_type': exam.event_type.pk,
        # 'repeat_type': exam.repeat_type.pk,
        # 'start_date': exam.start_date,
        # 'start_time': exam.start_time,
        # 'end_time': exam.end_time,
        'predicted_study_hours': predicted_study_hours,
        'predicted_weeks': predicted_weeks,
        'predicted_score': predicted_score,
        'final_study_hours': final_study_hours,
        'final_weeks': final_weeks,
        'final_score': final_score,
        'created_date': created_date,
        'event_id': event_id,
      })

      context['form'] = form
    # else:
    #   form = ExamForm(initial={
    #     'start_date': datetime.date.today()
    #   })

      context['form'] = form

    return render(request, 'exams/exam_detail.html', context)

def search(request):
  return render(request, 'exams/exam_search.html')