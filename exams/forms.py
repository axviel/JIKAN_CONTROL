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
  exam_number = forms.IntegerField(
    label='Exam Number', 
    widget=forms.NumberInput(attrs={
      'id': 'exam_number', 
      'class': 'form-control'}),
      max_value=3,
      min_value=1
    )
  created_date = forms.DateTimeField(
    label='Created Date', 
    widget=DateInput(attrs={
      'id': 'created_date', 
      'class': 'form-control'}),
      required=False
    )
