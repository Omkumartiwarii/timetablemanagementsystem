"""
Django settings for projttgs project.

Updated for Django 4.x compatibility.
"""

import os
from pathlib import Path

# ----------------------------
# BASE DIR
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------
# SECURITY
# ----------------------------
SECRET_KEY = '!^pl^(esc16%iofqa$k!2)!h_c*uedsi66(9ucvz1k-y=2ltk5'
DEBUG = True
ALLOWED_HOSTS = []

# ----------------------------
# INSTALLED APPS
# ----------------------------
INSTALLED_APPS = [
    'account',
    'ttgen',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# ----------------------------
# MIDDLEWARE
# ----------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ----------------------------
# ROOT URLCONF
# ----------------------------
ROOT_URLCONF = 'projttgs.urls'

# ----------------------------
# TEMPLATES
# ----------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ----------------------------
# WSGI
# ----------------------------
WSGI_APPLICATION = 'projttgs.wsgi.application'

# ----------------------------
# DATABASE
# ----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ----------------------------
# PASSWORD VALIDATION
# ----------------------------
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

# ----------------------------
# INTERNATIONALIZATION
# ----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ----------------------------
# STATIC FILES
# ----------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'assets'

# ----------------------------
# AUTHENTICATION
# ----------------------------
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'admindash'
LOGOUT_URL = 'logout'

# ----------------------------
# EMAIL SETTINGS
# ----------------------------
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''  # <-- put your Gmail here
EMAIL_HOST_PASSWORD = ''  # <-- put your Gmail App Password here
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# ----------------------------
# THIRD-PARTY
# ----------------------------
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# ----------------------------
# DEFAULT AUTO FIELD (Django 4.x)
# ----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'