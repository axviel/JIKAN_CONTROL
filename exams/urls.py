from django.urls import path
from . import views

urlpatterns = [
  path('list', views.index, name='exam_list'),
  path('detail/<int:exam_id>', views.exam, name='exam_detail'),
  path('detail/event/<int:event_id>', views.exam, name='exam_event_detail'),
  path('score', views.predict_score, name='exam_score'),
  path('hours', views.predict_study_hours, name='exam_hours'),
  path('number', views.get_next_exam_number, name='exam_number'),
  path('detail', views.exam, name='exam_detail'),
  path('search', views.search, name='exam_search'),
  path('remove', views.remove, name='exam_remove'),
  path('id', views.get_exam_id, name='exam_id'),
]