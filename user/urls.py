from django.urls import path
from . import views

urlpatterns = [
  path('user_detail', views.profile, name='user_detail'),
  path('password_change', views.password, name='password_change'),

]