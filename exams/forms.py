from django import forms
from .models import Exam
from .models import Event
from .models import Course

from django.db.models import Q

# todo Move later to a separate file (or app) that can be used in other apps' view.py
class DateInput(forms.DateInput):
  input_type = 'date'

class TimeInput(forms.TimeInput):
  input_type = 'time'

class EntityIdInput(forms.NumberInput):
  input_type = 'hidden'

# Used to create the input fields rendered in the template
class ExamForm(forms.Form):

  exam_id = forms.IntegerField(
    widget=EntityIdInput(attrs={
      'id': 'exam_id'}),
    required=False
    )
  title = forms.CharField(
    label='Title', 
    widget=forms.TextInput(attrs={
      'id': 'title', 
      'class': 'form-control'})
    )
  description = forms.CharField(
    label='Description', 
    widget=forms.Textarea(attrs={
      'id': 'description', 
      'class': 'form-control'})
    )
  exam_number = forms.IntegerField(
    label='Exam Number', 
    widget=forms.NumberInput(attrs={
      'id': 'exam_number', 
      'class': 'form-control'}),
      min_value=1
    )
  created_date = forms.DateTimeField(
    label='Created Date', 
    widget=DateInput(attrs={
      'id': 'created_date', 
      'class': 'form-control'}),
      required=False
    )
  # event = forms.ModelChoiceField(
  #   label='Event', 
  #   empty_label=None, 
  #   queryset= Event.objects.filter(Q(is_hidden=False, event_type_id=4) & Q(exam=None) ),
  #   widget=forms.Select(attrs={
  #     'id': 'event', 
  #     'class':'form-control'}),
  #     )
  event = forms.ModelChoiceField(
    label='Event', 
    empty_label=None, 
    queryset=Event.objects.all().filter(is_hidden=False, event_type_id=4), 
    widget=forms.Select(attrs={
      'id': 'event', 
      'class':'form-control'}),
      )
  # event = forms.ModelChoiceField(
  #   label='Event', 
  #   empty_label=None, 
  #   queryset=None, 
  #   widget=forms.Select(attrs={
  #     'id': 'event', 
  #     'class':'form-control'}),
  #     )
  course = forms.ModelChoiceField(
    label='Course', 
    empty_label=None, 
    queryset=Course.objects.all().filter(is_hidden=False), 
    widget=forms.Select(attrs={
      'id': 'course', 
      'class':'form-control'}),
      )
  predicted_study_hours = forms.IntegerField(
    label='Study Hours', 
    widget=forms.NumberInput(attrs={
      'id': 'predicted_study_hours', 
      'class': 'form-control'}),
      min_value=1,
    initial=0
    )
  predicted_score = forms.IntegerField(
    label='Exam Score', 
    widget=forms.NumberInput(attrs={
      'id': 'predicted_score', 
      'class': 'form-control'}),
    min_value=1,
    initial=0
    )
  final_study_hours = forms.IntegerField(
    label='Study Hours', 
    widget=forms.NumberInput(attrs={
      'id': 'final_study_hours', 
      'class': 'form-control'}),
    min_value=0,
    initial=0
    )
  final_score = forms.IntegerField(
    label='Exam Score', 
    widget=forms.NumberInput(attrs={
      'id': 'final_score', 
      'class': 'form-control'}),
    max_value=100,
    initial=0
    )