from django.contrib import admin
from django.contrib.auth import views as auth_views
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
    path('webpush/', include('webpush.urls')),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name="password_reset"),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name="password_reset_complete"),
]
