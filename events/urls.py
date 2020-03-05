from django.urls import path
from . import views

urlpatterns = [
  path('list', views.index, name='event_list'),
  path('detail/<int:event_id>', views.event, name='event_detail'),
  path('detail', views.event, name='event_detail'),
  path('search', views.search, name='event_search'),
]
