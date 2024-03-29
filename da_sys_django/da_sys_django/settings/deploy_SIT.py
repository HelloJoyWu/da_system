"""
Django settings for da_sys_django project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from .default import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'da-sys-dev-XxfU7jEQitObj3eAIGava_ZFIkQK46g-p4u2gpmSpVw'  # 'da-sys-dev-' + secrets.token_urlsafe(32)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# cache

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "unix://:redis4SYS@/redis_conn/sys_redis.sock",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600

STATIC_ROOT = '/static'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'simple':
            {'format': '[%(asctime)s] %(name)s - %(levelname)s - %(message)s'},
        'console':
            {'format': '[%(name)s] %(levelname)s - %(message)s'}
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'console',
            'filters': ['require_debug_true'],
            'stream': 'ext://sys.stdout'
        },
        'info_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'filename': '/tmp/log/info.log',  # think: how to use relative path!
            'maxBytes': 20971520,  # 20MB
            'backupCount': 20,
            'encoding': 'utf8'
            },
        'error_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'simple',
            'filename': '/tmp/log/error.log',  # think: how to use relative path!
            'maxBytes': 20971520,  # 20MB
            'backupCount': 20,
            'encoding': 'utf8'
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'filters': ['require_debug_false'],
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'info_file_handler', 'error_file_handler'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'info_file_handler', 'error_file_handler', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'info_file_handler', 'error_file_handler', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'recommender': {
            'handlers': ['console', 'info_file_handler', 'error_file_handler', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'dao': {
            'handlers': ['console', 'info_file_handler', 'error_file_handler', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'info_file_handler', 'error_file_handler'],
        'level': 'INFO',
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'dabot@adcrow.tech'
EMAIL_HOST_PASSWORD = 'uupjyfcesixutezh'
EMAIL_TIMEOUT = 5
SERVER_EMAIL = EMAIL_HOST_USER

ADMINS = [('rmpeter0474', 'rmpeter0474@adcrow.tech'), ]
MANAGERS = ADMINS
