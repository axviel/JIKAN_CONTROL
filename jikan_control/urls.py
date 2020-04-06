from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path(what you first want for those urls, app url file name)
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('events/', include('events.urls')),
    path('notes/', include('notes.urls')),
    path('courses/', include('courses.urls')),
    path('exams/', include('exams.urls')),
    path('user/', include('user.urls')),
    path('jikancalendar/', include('jikancalendar.urls')),
    path('admin/', admin.site.urls),
]
