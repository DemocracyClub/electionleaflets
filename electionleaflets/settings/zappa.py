import os

from .base import *  # noqa: F401,F403

if os.environ.get('SERVERTYPE', None) == 'AWS Lambda':
    GEOS_LIBRARY_PATH = '/opt/lib/libgeos_c.so'
    GDAL_LIBRARY_PATH = '/opt/lib/libgdal.so.26.0.0'

ALLOWED_HOSTS = ['*']

# Override the database name and user if needed
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': os.environ.get('DATABASE_HOST'),
        'USER': os.environ.get('DATABASE_USER'),
        'PORT': '5432',
        'NAME': os.environ.get('DATABASE_NAME'),
        'PASSWORD': os.environ.get('DATABASE_PASS')
    }
}

EMAIL_BACKEND = 'django_ses.SESBackend'
DEFAULT_FROM_EMAIL = 'hello@democracyclub.org.uk'
AWS_SES_REGION_NAME = 'eu-west-1'
AWS_SES_REGION_ENDPOINT = 'email.eu-west-1.amazonaws.com'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 's3_lambda_storage.S3StaticStorage'
STATICFILES_MANIFEST_NAME = os.environ.get('STATICFILES_MANIFEST_NAME')

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

THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.cached_db_kvstore.KVStore'

CSRF_TRUSTED_ORIGINS = ['.electionleaflets.org']
