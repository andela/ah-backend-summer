import dj_database_url
import os

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(env='DEVELOPMENT_DATABASE_URL', engine='django.db.backends.postgresql')
}

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')
