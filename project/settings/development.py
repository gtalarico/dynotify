# Application definition
from base import *

SECRET_KEY = '12!@#asdsasas12!#1232$16%f70qweq!@#!@#^9*m9q*$121212!@!@!@l3=rl'

DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS.append('debug_toolbar')

# USE SQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'portal',
#         # The following settings are not used with sqlite3:
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

# LOOGER JSON CONFIG
from .logger_config_local import LOGGER_CONFIG
LOGGING = LOGGER_CONFIG
