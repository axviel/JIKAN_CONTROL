from django.urls import path
from . import views

urlpatterns = [
  path('list', views.index, name='course_list'),
  path('detail/<int:course_id>', views.course, name='course_detail'),
  path('detail', views.course, name='course_detail'),
  path('search', views.search, name='course_search'),
  path('remove', views.remove, name='course_remove'),
]
