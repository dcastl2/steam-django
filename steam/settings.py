"""
Django settings for steam project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""


import os


################################################################################
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
################################################################################
BASE_DIR    = '/var/www/steam/'
PROJECT_DIR = os.path.join(BASE_DIR, 'content/');


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bk&$4h$-(-#g#@v5hp^74yi+=4p18(%yny(ufc%e^9=tif7x_('


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []


################################################################################
# Application definition
################################################################################
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'content',
    'djangobower',
    'django_nvd3',
    'django_tables2',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'steam.urls'
WSGI_APPLICATION = 'steam.wsgi.application'


################################################################################
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
################################################################################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


################################################################################
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
################################################################################
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True


################################################################################
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
################################################################################
BASE_URL    = 'http://steam.cct.lsu.edu/'
STATIC_URL  = '/static/'
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
MEDIA_ROOT  = BASE_DIR 
MEDIA_URL   = os.path.join(BASE_DIR, 'media/')
ALLOWED_INCLUDE_ROOTS =[MEDIA_ROOT,]


################################################################################
# Templates
################################################################################
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
         os.path.join(PROJECT_DIR, 'templates/'),
         '/usr/lib64/python2.7/site-packages/django/contrib/admin/templates/'
        ],
        'OPTIONS': {
           'context_processors': [
               'django.contrib.auth.context_processors.auth',
               'django.template.context_processors.media',
               'django.template.context_processors.request',
            ]
         }
    },
]



################################################################################
# Authentication model
################################################################################
AUTH_USER_MODEL = 'content.MyUser'


################################################################################
# Bower
################################################################################
STATICFILES_FINDERS = {
  'djangobower.finders.BowerFinder'
}

BOWER_COMPONENTS_ROOT = '/var/www/steam/components'

BOWER_INSTALLED_APPS = {
  'jquery#1.9',
  'underscore',
  'd3',
  'nvd3',
}

#print TEMPLATE_DIRS
