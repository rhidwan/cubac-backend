"""
Django settings for cubac project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.urls import reverse_lazy
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '==#x$1w7a)hc5n37mzh$5v!tz*pp_zef3=4yo5l-5_@%%vpa-_'

# SECURITY WARNING: don't run with debug turned on in production!

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'cubac.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'cubac.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases



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

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# 
#

print("base dir", BASE_DIR)
PDF_STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# STATIC_ROOT = os.path.join(BASE_DIR, "static/")
AUTH_USER_MODEL = 'user.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'user.serializers.UserSerializer',
}
#django-allauth config
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/?verification=1'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/?verification=1'
ACCOUNT_ADAPTER = 'user.adapters.CustomUserAccountAdapter'

SITE_ID = 1
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


#bkash config

BKASH_APP_KEY = 'abcdxx2369'
 # bkash app key
BKASH_APP_SECRET = 'bkashSup3rS3cRet'
BKASH_APP_USERNAME ='sandboxTestUser' 
BKASH_APP_PASSWORD =  'sandboxTestPassword'
# BKASH_APP_VERSION = // bkash app version
BKASH_APP_BASE_URL = 'https://checkout.sandbox.bka.sh/v1.2.0-beta' #// bkash app base url
BKASH_APP_PAYMENT_TOKEN_GRANT_URL = '%s/checkout/token/grant' % (BKASH_APP_BASE_URL)
BKASH_APP_PAYMENT_CREATE_URL = '%s/checkout/payment/create' % (BKASH_APP_BASE_URL)
BKASH_APP_PAYMENT_EXECUTE_URL = '%s/checkout/payment/execute' % (BKASH_APP_BASE_URL)

#sslcommerz config
SSL_STORE_ID = 'chitt62824a465e6b1'
SSL_STORE_SECRET = 'chitt62824a465e6b1@ssl'

DJANGORESIZED_DEFAULT_SIZE = [300, 300]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True


LOGIN_URL = reverse_lazy('login')