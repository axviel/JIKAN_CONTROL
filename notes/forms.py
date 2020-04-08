from django import forms
from .models import Event

# todo Move later to a separate file (or app) that can be used in other apps' view.py
class DateInput(forms.DateInput):
  input_type = 'date'

class TimeInput(forms.TimeInput):
  input_type = 'time'

class EntityIdInput(forms.NumberInput):
  input_type = 'hidden'

# Used to create the input fields rendered in the template
class NotesForm(forms.Form):
  note_id = forms.IntegerField(
    widget=EntityIdInput(attrs={
      'id': 'note_id'}),
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
  created_date = forms.DateTimeField(
    label='Created Date', 
    widget=DateInput(attrs={
      'id': 'created_date', 
      'class': 'form-control'}),
      required=False
   )
  event = forms.ModelChoiceField( 
    label='Event',
    empty_label=None,
    queryset=Event.objects.filter(is_hidden=False),
    widget=forms.Select(attrs={
      'id':'event',
      'class': 'form-control'})
   )
