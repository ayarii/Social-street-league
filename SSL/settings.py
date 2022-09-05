"""
Django settings for SSL project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from email.policy import default
import environ
import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j^^t^y&sp=b2ki2dg9)pg@5m)a@0lhu0y&z0lpf5cs8)$0^7we'
# SECRET_KEY = 'django-insecure-j^^t^y&sp=b2ki2dg9)pg@5m)a@0lhu0y&z0lpf5cs8)$0^7we'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = ( 
    'django.contrib.auth.backends.AllowAllUsersModelBackend', 
    'users.backends.CaseInsensitiveModelBackend',
    )


GDAL_LIBRARY_PATH = r'D:\stage\SSL\Lib\site-packages\osgeo\gdal304.dll'
GEOS_LIBRARY_PATH = r'D:\stage\SSL\Lib\site-packages\osgeo\geos_c.dll'

# Application definition

INSTALLED_APPS = [
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'leaflet',
    'django.contrib.gis',
    'djgeojson',
    'widget_tweaks',
    'users',
    'activity',
    'event',
    'home',
    'post',
    'sponsor',
    'team',
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

ROOT_URLCONF = 'SSL.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                
    
            ],
        },
    },
]

WSGI_APPLICATION = 'SSL.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/



STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATICFILES_DIRS =[
    os.path.join(BASE_DIR,'SSL/static')
    ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATA_UPLOAD_MAX_MEMORY_SIZE=10760485
#MEDIA IS HERE
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

#map setting run pip install django-location-field


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER =  'socialstreetleague@gmail.com'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'socialstreetleague@gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = 'ksizsxorvstapzkx'

