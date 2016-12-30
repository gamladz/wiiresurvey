from .base import *

import dj_database_url

DEBUG = dotenv.get('DEBUG')
ALLOWED_HOSTS = ['*']

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {
    'default': dj_database_url.config()
}

DATABASES['default']['CONN_MAX_AGE'] = 500
