from django.urls import path
from . import views

urlpatterns = [
  path('list', views.index, name='event_list'),
  path('detail/<int:event_id>', views.event, name='event_detail'),
  path('detail', views.event, name='event_detail'),
  path('search', views.search, name='event_search'),
  path('remove', views.remove, name='event_remove'),
  path('complete', views.complete, name='event_complete'),
]
