import os
from .base import *  # noqa: F401,F403

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DATABASE_HOST"),
        "USER": "postgres",
        "PORT": "5432",
        "NAME": os.environ.get("POSTGRES_DATABASE_NAME"),
        "PASSWORD": os.environ.get("DATABASE_PASS"),
    }
}
SECRET_KEY = os.environ.get("SECRET_KEY")

EMAIL_BACKEND = "django_ses.SESBackend"
DEFAULT_FROM_EMAIL = "hello@democracyclub.org.uk"
AWS_SES_REGION_NAME = "eu-west-2"
AWS_SES_REGION_ENDPOINT = "email.eu-west-2.amazonaws.com"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_STORAGE_BUCKET_NAME = os.environ.get("LEAFLET_IMAGES_BUCKET_NAME")
AWS_S3_SECURE_URLS = True
AWS_S3_HOST = "s3-eu-west-2.amazonaws.com"
# TODO
# AWS_S3_CUSTOM_DOMAIN = "data.electionleaflets.org"


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "el_cache",
    }
}

THUMBNAIL_KVSTORE = "sorl.thumbnail.kvstores.cached_db_kvstore.KVStore"
THUMBNAIL_BACKEND = "core.s3_thumbnail_store.S3Backend"

CSRF_TRUSTED_ORIGINS = [".electionleaflets.org"]
USE_X_FORWARDED_HOST = True

setup_sentry()
