from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='event_list'),
  path('<int:event_id>', views.event, name='event_detail'),
  path('search', views.search, name='event_search'),
]
