from django.urls import path
from . import views

urlpatterns = [
  path('list', views.index, name='note_list'),
  path('detail/<int:note_id>', views.note, name='note_detail'),
  path('detail', views.note, name='note_detail'),
  path('search', views.search, name='note_search'),
  path('remove', views.remove, name='note_remove'),
]
