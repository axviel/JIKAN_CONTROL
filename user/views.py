from django.shortcuts import render


def profile(request):
  return render(request, 'user/user_detail.html')
