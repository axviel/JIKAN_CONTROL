from django.urls import path
from . import views

urlpatterns = [
  path('user_detail', views.profile, name='user_detail'),

]