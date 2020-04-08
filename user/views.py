from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .forms import UserForm

def profile(request):
  if not request.user.is_authenticated:
    messages.error(request, 'Unauthorized. Must be logged in')
    return redirect('login')

  if request.method == "POST":
    # Get the POST form
    form = UserForm(request.POST)

    if form.is_valid():
      username = form.cleaned_data['username']
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email = form.cleaned_data['email']

      user_model = get_user_model()
    
      user, is_created = user_model.objects.update_or_create(
            id=request.user.id,
            defaults={
              'username': username,
              'first_name': first_name,
              'last_name': last_name,
              'email': email
              },
        )
      # Save in the db
      user.save()

      # UI success message
      messages.success(request, 'Profile updated successfully')
      context = {
        'form': form
      }
      return render(request, 'user/user_detail.html', context)
    
    # Form was invalid, so return it
    context = {
      'form': form
    }

    # UI error message
    messages.error(request, 'Profile was not updated')

    return render(request, 'user/user_detail.html', context)


  else:
    user_model = get_user_model()

    user = get_object_or_404(user_model, pk=request.user.id)

    context = {}

    form = UserForm(initial={
      'username': user.username,
      'first_name': user.first_name,
      'last_name': user.last_name,
      'email': user.email,
      'password': user.password
    })

    context['form'] = form
    return render(request, 'user/user_detail.html', context)
