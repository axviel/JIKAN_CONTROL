from django import forms
from .models import Exam

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
  predicted_study_hours = forms.IntegerField(
    widget=EntityIdInput(attrs={
      'id': 'predicted_study_hours'})
    )
  predicted_weeks = forms.IntegerField(
    widget=EntityIdInput(attrs={
      'id': 'predicted_weeks'})
    )
  predicted_score = forms.IntegerField(
    widget=EntityIdInput(attrs={
      'id': 'predicted_score'}),
    )
  final_study_hours = forms.IntegerField(
    widget=EntityIdInput(attrs={
      'id': 'final_study_hours'}),
    )
  final_weeks = forms.IntegerField(
    widget=EntityIdInput(attrs={
      'id': 'final_weeks'}),
    )
  final_score = forms.IntegerField(
    widget=EntityIdInput(attrs={
      'id': 'final_score'}),
    )
  created_date = forms.IntegerField(
    widget=EntityIdInput(attrs={
      'id': 'created_date'}),
    )
  event_id = forms.IntegerField(
    widget=EntityIdInput(attrs={
      'id': 'event_id'}),
    )
#   start_time = forms.TimeField(
#     label='Start Time', 
#     widget=TimeInput(attrs={
#       'id': 'start_time', 
#       'class': 'form-control'})
#     )
#   end_time = forms.TimeField(
#     label='End Time', 
#     widget=TimeInput(attrs={
#       'id': 'end_time', 
#       'class': 'form-control'})
#     )
#   start_date = forms.DateTimeField(
#     label='Start Date', 
#     widget=DateInput(attrs={
#       'id': 'start_date', 
#       'class': 'form-control'})
#       )
#   end_date = forms.DateTimeField(
#     label='End Date', 
#     widget=DateInput(attrs={
#       'id': 'end_date', 
#       'class': 'form-control'}),
#     required=False
#       )
#   event_type = forms.ModelChoiceField(
#     label='Event Type', 
#     empty_label=None, 
#     queryset=EventType.objects.all(), 
#     widget=forms.Select(attrs={
#       'id': 'event_type', 
#       'class':'form-control'})
#       )
#   repeat_type = forms.ModelChoiceField(
#     label='Repeat Type', 
#     empty_label=None, 
#     queryset=RepeatType.objects.all(), 
#     widget=forms.Select(attrs={
#       'id': 'repeat_type', 
#       'class':'form-control'})
#       )
