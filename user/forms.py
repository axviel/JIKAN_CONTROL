from django import forms

# Used to create the input fields rendered in the template
class UserForm(forms.Form):
  first_name = forms.CharField(
    label='First Name', 
    widget=forms.TextInput(attrs={
      'id': 'first_name', 
      'class': 'form-control'})
    )
  last_name = forms.CharField(
    label='Last Name', 
    widget=forms.TextInput(attrs={
      'id': 'last_name', 
      'class': 'form-control'})
    )
  email = forms.CharField(
    label='Email', 
    widget=forms.TextInput(attrs={
      'id': 'email', 
      'class': 'form-control'})
    )
  password = forms.CharField(
    label='Password', 
    widget=forms.PasswordInput(attrs={
      'id': 'password', 
      'class': 'form-control'}),
      required=False
    )
