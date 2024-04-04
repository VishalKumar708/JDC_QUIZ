"""
Django settings for JDC project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--5tykl@tfh76#0)(b*_+(n(-x5xt#&pei4*hlfk4u+%^6opvo1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    "User",
    "Quiz_Api",
    "phonenumber_field",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # custom middlewares
    'utils.middleware.ValidateURLMiddleware',
    'utils.middleware.JSONCheckMiddleware',
    'utils.middleware.InternalServerErrorMiddleware',
    # 'utils.middleware.CustomizeResponseMiddleware',
    'utils.middleware.QueryCountMiddleware'

]

ROOT_URLCONF = 'JDC.urls'
AUTH_USER_MODEL = 'User.User'
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

WSGI_APPLICATION = 'JDC.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jdc_quiz',
        'USER': 'root',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# AUTH_USER_MODEL = 'User.User'

# REST FRAMEWORK settings
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.Pagination',
    'PAGE_SIZE': 20, # Default page size
    # 'DEFAULT_PAGE_SIZE': 150
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}


# SWAGGER settings
SWAGGER_SETTINGS = {
    'VALIDATOR_URL': 'http://localhost:8189',

}


# # *************************    Django Logger   ****************************

LOG_DIR = os.path.join(BASE_DIR, 'log')

# Ensure the log directory exists, and create it if it doesn't
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s | %(asctime)s| path: %(pathname)s | func: %(funcName)s | line_no: %(lineno)s | %(message)s",
        },
        "plane": {
            "format": "%(levelname)s: %(asctime)s | %(module)s.py| func: %(funcName)s| line number: %(lineno)s| %(message)s",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        'info': {
            "level": "INFO",
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, "info.log"),
            'maxBytes': 30 * 1024 * 1024,
            'backupCount': 10,
            "formatter": "verbose",
            "encoding": 'utf-8'
        },
        'error': {
            "level": "ERROR",
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, "error.log"),
            'maxBytes': 90 * 1024 * 1024,
            'backupCount': 10,
            "formatter": "verbose",
            "encoding": 'utf-8'
        },
        'warning': {
            "level": "WARNING",
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, "warning.log"),
            'maxBytes': 30 * 1024 * 1024,
            'backupCount': 10,
            "formatter": "verbose",
            "encoding": 'utf-8'
        },
        'terminal': {
            "level": "INFO",
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, "console.log"),
            # 'maxBytes': 30 * 1024 * 1024,
            'backupCount': 10,
            "formatter": "verbose",
            "encoding": 'utf-8'
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "terminal"],
            "propagate": False,
            "level": "INFO"
        },
        "info": {
            "handlers": ["info"],
            "propagate": False,
            "level": "INFO"
        },
        "error": {
            "handlers": ["error"],
            "level": "ERROR",
            "propagate": False,
        },
        "warning": {
            "handlers": ["warning"],
            "level": "WARNING",
            "propagate": False,
        }


    },
    "root": {
        "handlers": ["info", "error", "console"],  # Send messages to both info and error handlers
        "level": "INFO",
    },
}

# Global variables
DEFAULT_DATE_FORMAT = "%d %B, %Y"
APPEND_SLASH = False
