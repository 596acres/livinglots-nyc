import os

from .base import *

ADMINS = (
    ('', 'admin@livinglotsnyc.org'),
)

MANAGERS = (
    ('', 'admin@livinglotsnyc.org'),
)

FACILITATORS = {
    'global': [
        'facilitators@livinglotsnyc.org',
    ],
}

ALLOWED_HOSTS = get_env_variable('ALLOWED_HOSTS').split(',')

#
# django-cachalot
#

INSTALLED_APPS += (
    'cachalot',
)
CACHES = {
    'default': {
        'BACKEND': 'caching.backends.memcached.MemcachedCache',
        'LOCATION': [
            get_env_variable('MEMCACHE_LOCATION'),
        ],
    },
}


#
# email
#
INSTALLED_APPS += (
    'mailer',
)
EMAIL_BACKEND = 'mailer.backend.DbBackend'
EMAIL_HOST = get_env_variable('EMAIL_HOST')
EMAIL_HOST_USER = get_env_variable('EMAIL_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = get_env_variable('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = get_env_variable('SERVER_EMAIL')


#
# logging
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'log_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT, '../logs', 'django.log'),
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['log_file', 'mail_admins'],
        'level': 'WARNING',
    },
}


#
# SSL
#
# TODO uncomment for SSL
#CSRF_COOKIE_SECURE = True
#SESSION_COOKIE_SECURE = True

LOT_CENTROIDS_URL = get_env_variable('TILES_BASE') + '/lots-centroids/'
LOT_POLYGONS_URL = get_env_variable('TILES_BASE') + '/lots-polygons/'
PARCELS_URL = get_env_variable('TILES_BASE') + '/parcels/'

#
# CORS
#
CORS_ORIGIN_REGEX_WHITELIST = ('^(https?://)?(\w+\.)?nycommons\.org$',)
