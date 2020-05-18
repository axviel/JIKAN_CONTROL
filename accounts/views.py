from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User

def signup(request):
  if request.method == 'POST':
    # Get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Check if passwords match
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        # Show error
        messages.error(request, 'Username already taken')
        return redirect('signup')
      else:
        # Check email
        if User.objects.filter(email=email).exists():
          # Show error
          messages.error(request, 'Email already taken')
          return redirect('signup')
        else:
          # Create the user
          user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
          user.save()
          # Show success 
          messages.success(request, 'Registration successful and you can now login')
          return redirect('login')
    else:
      # Show error
      messages.error(request, 'Passwords do not match')
      return redirect('signup')
  else:
    return render(request, 'accounts/signup.html')

def login(request):
  if request.method == 'POST':
    # Get fields
    username = request.POST['username']
    password = request.POST['password']

    # Validate
    user = auth.authenticate(username=username, password=password)
    if user is not None:
      # Login user
      auth.login(request, user)
      # Show success 
      # messages.success(request, 'Login successful')
      return redirect('calendar')
    else:
      # Show error
      messages.error(request, 'Invalid username or password')
      return redirect('login')
  else:
    return render(request, 'accounts/login.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    # Show success 
    messages.success(request, 'Logout successful')
    return redirect('index')

def dashboard(request):
  # return render(request, 'accounts/dashboard.html')
  return redirect('calendar')