"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path


# Environment, must be "production" or "development"
ENVIRONMENT = os.environ.get("ENVIRONMENT") or "production"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY") or 'secret'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if (ENVIRONMENT == "development"):
    DEBUG = True

ALLOWED_HOSTS = []
if (ENVIRONMENT == "development"):
    ALLOWED_HOSTS = ALLOWED_HOSTS + [
        "*"
    ]

# Application definition
INSTALLED_APPS = [
    'new_releases',

    'rest_framework',
    'django_celery_beat',
    'django_celery_results',

    'django_extensions',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
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

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME') or 'app',
        'USER': os.environ.get('DB_USER') or 'user',
        'PASSWORD': os.environ.get('DB_PASSWORD') or 'password',
        'HOST': os.environ.get('DB_HOST') or 'localhost',
        'PORT': os.environ.get('DB_PORT') or 5432
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# Spotify Web API Configuration

SPOTIFY_CLIENT_ID = os.environ.get("CLIENT_ID")

SPOTIFY_CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

# Interval duration (in seconds) between every refresh
SPOTIFY_ARTISTS_REFRESH_INTERVAL = 30.0

# Callback endpoint for OAuth2 spotify auth
SPOTIFY_CALLBACK_URL = os.environ.get("SPOTIFY_CALLBACK_URL") or "http://localhost:5000/auth"

SPOTIFY_AUTH_SCOPE = "user-read-email user-read-private"

# Celery configuration

CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672/celeryhost'

CELERY_RESULT_BACKEND = 'django-db'

# If time zones are active (USE_TZ = True) define your local

CELERY_TIMEZONE = 'Europe/Paris'

# We're going to have our tasks rolling soon, so that will be handy

CELERY_BEAT_SCHEDULE = {
    'synchronize_artists': {
        'task': 'new_releases.tasks.synchronize_artists.synchronize_artists',
        'schedule': SPOTIFY_ARTISTS_REFRESH_INTERVAL
    }
}
