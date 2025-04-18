import os

from django.urls import set_urlconf

from .base import *  # noqa: F401,F403

ALLOWED_HOSTS = [os.environ.get("APP_DOMAIN")]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ["DATABASE_HOST"],
        "USER": os.environ["DATABASE_USER"],
        "PORT": "5432",
        "NAME": os.environ["DATABASE_NAME"],
        "PASSWORD": os.environ["DATABASE_PASS"],
    }
}
SECRET_KEY = os.environ.get("SECRET_KEY")

EMAIL_BACKEND = "django_ses.SESBackend"
DEFAULT_FROM_EMAIL = "hello@democracyclub.org.uk"
AWS_SES_REGION_NAME = "eu-west-2"
AWS_SES_REGION_ENDPOINT = "email.eu-west-2.amazonaws.com"

PIPELINE["PIPELINE_ENABLED"] = True  # noqa
PIPELINE["PIPELINE_COLLECTOR_ENABLED"] = False  # noqa

WHITENOISE_AUTOREFRESH = False
WHITENOISE_STATIC_PREFIX = "/static/"

STATIC_URL = WHITENOISE_STATIC_PREFIX
STATICFILES_STORAGE = "electionleaflets.storages.StaticStorage"
STATICFILES_DIRS = (root("assets"),)  # noqa: F405
STATIC_ROOT = root("static")  # noqa: F405
MEDIA_ROOT = root(  # noqa: F405
    "media",
)
MEDIA_URL = "/media/"
set_urlconf(ROOT_URLCONF)  # noqa: F405

AWS_DEFAULT_ACL = "public-read"

DEFAULT_FILE_STORAGE = "electionleaflets.storages.TempUploadS3MediaStorage"

AWS_STORAGE_BUCKET_NAME = os.environ.get("LEAFLET_IMAGES_BUCKET_NAME")
AWS_S3_SECURE_URLS = True
AWS_S3_HOST = "s3-eu-west-2.amazonaws.com"
AWS_S3_CUSTOM_DOMAIN = f"images.{os.environ.get('APP_DOMAIN')}"
AWS_S3_USE_SSL = True
AWS_S3_REGION_NAME = "eu-west-2"

WSGI_APPLICATION = "electionleaflets.wsgi.application"


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "el_cache",
    }
}

THUMBNAIL_KVSTORE = "sorl.thumbnail.kvstores.cached_db_kvstore.KVStore"
THUMBNAIL_BACKEND = "core.s3_thumbnail_store.S3Backend"

CSRF_TRUSTED_ORIGINS = ["https://electionleaflets.org"]
USE_X_FORWARDED_HOST = True

YNR_API_KEY = os.environ["YNR_API_KEY"]  # Fail if not API key

setup_sentry()  # noqa: F405
