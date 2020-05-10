from bootstrap_datepicker_plus import TimePickerInput
from django import forms
from .models import EventType, RepeatType

# todo Move later to a separate file (or app) that can be used in other apps' view.py
class DateInput(forms.DateInput):
  input_type = 'date'

class TimeInput(forms.TimeInput):
  input_type = 'time'

class EntityIdInput(forms.NumberInput):
  input_type = 'hidden'

# Used to create the input fields rendered in the template
class EventForm(forms.Form):
  event_id = forms.IntegerField(
    widget=EntityIdInput(attrs={
      'id': 'event_id'}),
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
  start_time = forms.TimeField(
    label='Start Time', 
    widget =TimePickerInput(attrs={
      'id': 'start_time',
      'class': 'form-control'})
    )
  end_time = forms.TimeField(
    label='End Time', 
    widget=TimeInput(attrs={
      'id': 'end_time', 
      'class': 'form-control'})
    )
  start_date = forms.DateTimeField(
    label='Start Date', 
    widget=DateInput(attrs={
      'id': 'start_date', 
      'class': 'form-control'})
      )
  end_date = forms.DateTimeField(
    label='End Date', 
    widget=DateInput(attrs={
      'id': 'end_date', 
      'class': 'form-control'}),
    required=False
      )
  event_type = forms.ModelChoiceField(
    label='Event Type', 
    empty_label=None, 
    queryset=EventType.objects.all(), 
    widget=forms.Select(attrs={
      'id': 'event_type', 
      'class':'form-control'})
      )
  repeat_type = forms.ModelChoiceField(
    label='Repeat Type', 
    empty_label=None, 
    queryset=RepeatType.objects.all(), 
    widget=forms.Select(attrs={
      'id': 'repeat_type', 
      'class':'form-control'})
      )
