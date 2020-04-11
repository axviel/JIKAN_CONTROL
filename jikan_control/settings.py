import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '%(6x$n*nvb56ms#w#s232&+z&$0gy$m-1!u2ve22x+s1re0zey'
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.environ.get('DJANGO_DEBUG') == 'True')
# DEBUG = 'True'

SQLALCHEMY_TRACK_MODIFICATIONS=False

ALLOWED_HOSTS = ['jikancontrol.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'pages.apps.PagesConfig',
    'jikancalendar.apps.JikancalendarConfig',
    'events.apps.EventsConfig',
    'eventtypes.apps.EventtypesConfig',
    'repeattypes.apps.RepeattypesConfig',
    'accounts.apps.AccountsConfig',
    'notes.apps.NotesConfig',
    'exams.apps.ExamsConfig',
    'courses.apps.CoursesConfig',
    'examstudy.apps.ExamstudyConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webpush',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jikan_control.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BE67B3w1HywCEpjnZ1AKhmKefMDdqGFIloMeahozj2T87E-65Vn9KS-KCryi7mNGMHw9Pvrb8XIPs5ZBgG2o-Tc",
    "VAPID_PRIVATE_KEY":"yLBzNha1wF9TVxjoub5kPMrT8wTnyHrJe980HPds8a8",
    "VAPID_ADMIN_EMAIL": "admin@example.com"
}

WSGI_APPLICATION = 'jikan_control.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jikan_control_db',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': 'localhost'
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'jikan_control/static')
]

# Messages
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

django_heroku.settings(locals())
