from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='note_list'),
  path('<int:note_id>', views.note, name='note_detail'),
  path('search', views.search, name='note_search'),
]