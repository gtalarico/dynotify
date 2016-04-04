from base import *
import os

SECRET_KEY = os.environ['SECRET_KEY']

# Update database configuration with $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Allow all host headers
# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['dynotify.herokuapp.com']

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# If FORCE_DEBUG is set, force debug
DEBUG = bool(os.environ.get('DJANGO_FORCE_DEBUG', None))

from .logger_config_deploy import LOGGER_CONFIG
LOGGING = LOGGER_CONFIG
