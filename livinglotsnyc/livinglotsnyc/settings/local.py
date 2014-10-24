from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
TASTYPIE_FULL_DEBUG = DEBUG

ADMINS = (
    ('Admin', 'admin@example.com'),
)

MANAGERS = ADMINS

FACILITATORS = {
    'global': ['facilitator@example.com',],
}

TIME_ZONE = 'America/New_York'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT, '../logs', 'django.log'),
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
    },
    'root': {
        'handlers': ['log_file',],
        'level': 'DEBUG',
    },
}


#
# Django extensions
#

INSTALLED_APPS += (
    'django_extensions',
)


#
# debug toolbar settings
#

INTERNAL_IPS = ('127.0.0.1',)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOT_CENTROIDS_URL = "http://localhost:8080/lots-centroids/"
LOT_POLYGONS_URL = "http://localhost:8080/lots-polygons/"
PARCELS_URL = "http://localhost:8080/parcels/"
