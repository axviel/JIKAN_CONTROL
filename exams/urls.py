from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='exam_list'),
  path('<int:exam_id>', views.exam, name='exam_detail'),
  path('search', views.search, name='exam_search'),
]