from django.shortcuts import render, redirect

def index(request):
  # return render(request, 'pages/index.html')
  if not request.user.is_authenticated:
    return redirect('login')

  return redirect('calendar')

def about(request):
  return render(request, 'pages/about.html')
