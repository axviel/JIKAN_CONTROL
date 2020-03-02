from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('events/', include('events.urls')),
    path('notes/', include('notes.urls')),
    path('exams/', include('exams.urls')),
    path('jikancalendar/', include('jikancalendar.urls')),
    path('admin/', admin.site.urls),
]
