import os

from .base import *

GEOS_LIBRARY_PATH = '/var/task/libgeos_c.so'

ALLOWED_HOSTS = ['*']

# Override the database name and user if needed
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'electionleaflets',
        'USER': 'electionleaflets',
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': '5432',
        'PASSWORD': os.environ.get('DATABASE_PASS')
    }
}

DEFAULT_FILE_STORAGE = 's3_lambda_storage.S3LambdaStorage'
AWS_STORAGE_BUCKET_NAME = "data.electionleaflets.org"
AWS_S3_SECURE_URLS = True
AWS_S3_HOST = 's3-eu-west-1.amazonaws.com'
AWS_S3_CUSTOM_DOMAIN = "data.electionleaflets.org"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'el_cache',
    }
}

THUMBNAIL_KVSTORE ='sorl.thumbnail.kvstores.cached_db_kvstore.KVStore'

CSRF_TRUSTED_ORIGINS = ['.electionleaflets.org']
