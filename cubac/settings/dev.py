import os
from pathlib import Path

DEBUG = True

ALLOWED_HOSTS = ['*']
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).parent

print("base dir dev", BASE_DIR)
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'rest_framework',
    'rest_auth',
    'rest_auth.registration',
    'crispy_forms',
    'debug_toolbar',
    'user',
    'functions',
    'home',
    
    'profiles',
    'call_applications',
    'applications',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

