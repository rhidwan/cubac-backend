
from pathlib import Path
import os


DEBUG = False

ALLOWED_HOSTS = ['*']
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).parent

print("base dir prod", BASE_DIR)
# ALLOWED_HOSTS = ['www.cubac.online']


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
    'user',
    'functions',
    'home',
    
    'profiles',
    'call_applications',
    'applications',


]


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': "",
    }
}


STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
