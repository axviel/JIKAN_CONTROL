from django.urls import path
from . import views

urlpatterns = [
  path('list', views.index, name='exam_list'),
  path('detail/<int:exam_id>', views.exam, name='exam_detail'),
  path('detail', views.exam, name='exam_detail'),
  path('search', views.search, name='exam_search'),
  path('remove', views.remove, name='exam_remove'),
]