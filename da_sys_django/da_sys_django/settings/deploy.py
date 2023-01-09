from .default import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'da-sys-DZBJD3xg5xEs0dRdAj5Iq_hEJuBQzXQItfgZE9CfbCl0DBBwJsyBbIXtIpL0kL8lTc6b-9AF2oSvhNu7HiPzdQ'  # 'da-sys-' + secrets.token_urlsafe(64)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'daSystem',
        'USER': 'DAxAthena_aries',
        'PASSWORD': '2heDq9KY_xBVbS',
        'HOST': '10.9.24.90',
        'PORT': 3306,
        'OPTIONS': {
            'init_command': "SET TIME_ZONE='+00:00', default_storage_engine=INNODB"
        }
    },
    'maria_read': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cypress',
        'USER': 'DAxPeter_aries',
        'PASSWORD': 'PYG0a7aAv_eGx39',
        'HOST': '10.9.24.91',
        'PORT': 3306,
        'OPTIONS': {
            'isolation_level': 'READ UNCOMMITTED',
            'init_command': "SET TIME_ZONE='+00:00'"
        },
    },
}

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

STATIC_ROOT = BASE_DIR / 'static/'

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
            {'format': '[%(asctime)s] %(levelname)s - %(name)s - %(message)s'},
        'console':
            {'format': '[%(name)s] %(levelname)s - %(message)s'}
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'console',
            'filters': ['require_debug_true'],
            'stream': 'ext://sys.stdout'
        },
        'info_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'filename': '/tmp/log/da_sys_info.log',
            'maxBytes': 20971520,  # 20MB
            'backupCount': 20,
            'encoding': 'utf8'
            },
        'error_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'simple',
            'filename': '/tmp/log/da_sys_error.log',
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
        'rmsys': {
            'handlers': ['console', 'info_file_handler', 'error_file_handler', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'api': {
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

