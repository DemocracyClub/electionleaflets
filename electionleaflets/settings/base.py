import os
import sys
from os import environ

# PATH vars
from os.path import abspath, dirname, join

import dc_design_system


def here(x):
    return join(abspath(dirname(__file__)), x)


PROJECT_ROOT = here("..")


def root(x):
    return join(abspath(PROJECT_ROOT), x)


sys.path.insert(0, root("apps"))


DEBUG = False
template_DEBUG = DEBUG
TEMPLATE_DEBUG = DEBUG

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# DATABASES define in environment specific settings file
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "electionleaflets",
    }
}


TIME_ZONE = "Europe/London"
LANGUAGE_CODE = "en-GB"

ALLOWED_HOSTS = ["*"]

MEDIA_ROOT = root(
    "media",
)
MEDIA_URL = "/media/"
STATIC_ROOT = root("static")
STATIC_URL = "/static/"
STATICFILES_DIRS = (root("assets"),)

DEFAULT_FILE_STORAGE = "electionleaflets.storages.TempUploadLocalMediaStorage"
AWS_S3_FILE_OVERWRITE = False
STATICFILES_MANIFEST_NAME = environ.get(
    "STATICFILES_MANIFEST_NAME", "staticfiles.json"
)
AWS_STORAGE_BUCKET_NAME = "data.electionleaflets.org"
AWS_S3_SECURE_URLS = True
# AWS_S3_HOST = "s3-eu-west-1.amazonaws.com"
# AWS_S3_CUSTOM_DOMAIN = "data.electionleaflets.org"

PIPELINE = {
    "COMPILERS": ("pipeline.compilers.sass.SASSCompiler",),
    "SASS_BINARY": "pysassc",
    "CSS_COMPRESSOR": "pipeline.compressors.NoopCompressor",
    "STYLESHEETS": {
        "styles": {
            "source_filenames": [
                "scss/styles.scss",
                "scss/vendor/filepond.css",
                "scss/vendor/filepond-plugin-image-preview.css",
            ],
            "output_filename": "scss/styles.css",
            "extra_context": {
                "media": "screen,projection",
            },
        },
    },
    "JAVASCRIPT": {
        "scripts": {
            "source_filenames": [
                "javascript/app.js",
                "javascript/vendor/filepond.js",
                "javascript/vendor/filepond-plugin-image-exif-orientation.js",
                "javascript/vendor/filepond-plugin-image-preview.js",
                "javascript/image_uploader.js",
                # "javascript/vendor/ImageEditor.js",
            ],
            "output_filename": "app.js",
        }
    },
}


PIPELINE["CSS_COMPRESSOR"] = "pipeline.compressors.NoopCompressor"
PIPELINE["JS_COMPRESSOR"] = "pipeline.compressors.NoopCompressor"


PIPELINE["SASS_ARGUMENTS"] = (
    " -I " + dc_design_system.DC_SYSTEM_PATH + "/system"
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pipeline.finders.CachedFileFinder",
    "pipeline.finders.PipelineFinder",
    "pipeline.finders.ManifestFinder",
)

WHITENOISE_STATIC_PREFIX = "/static/"

SITE_ID = 1
SITE_LOGO = "images/logo.png"
USE_I18N = False
USE_L10N = True
LOGIN_URL = "/"

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = "/admin_media/"

# Don't share this with anybody.
SECRET_KEY = "elyfryi8on!dmw&8b3j-g0yve4u&%4_6%(tf3*)@#&mq*$yzhf^6"

MIDDLEWARE = (
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "s3file.middleware.S3FileMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "leaflets.middleware.SourceTagMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
    "dj_pagination.middleware.PaginationMiddleware",
)

ROOT_URLCONF = "electionleaflets.urls"
WSGI_APPLICATION = "electionleaflets.wsgi.application"

LEAFLET_APPS = [
    "core",
    "leaflets",
    "analysis",
    "elections",
    "people",
    "constituencies",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.forms",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "django.contrib.humanize",
    "dj_pagination",
    "rest_framework",
    "sorl.thumbnail",
    "storages",
    "uk_political_parties",
    "markdown",
    "django_extensions",
    "pipeline",
    "dc_design_system",
    "django_static_jquery",
    "s3file",
    "debug_toolbar",
    "django_filters",
    "dc_utils",
] + LEAFLET_APPS


def setup_sentry(environment=None):
    SENTRY_DSN = os.environ.get("SENTRY_DSN")
    if not SENTRY_DSN:
        return

    if not environment:
        environment = os.environ["DC_ENVIRONMENT"]
    release = os.environ.get("GIT_HASH", "unknown")
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        environment=environment,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
        release=release,
    )


THUMBNAIL_FORMAT = "PNG"
THUMBNAIL_KVSTORE = "sorl.thumbnail.kvstores.cached_db_kvstore.KVStore"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            root("templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.request",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.contrib.auth.context_processors.auth",
            ]
        },
    }
]
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_PAGINATION_CLASS": "api.helpers.LargerPageNumberPagination",
}


THANKYOU_MESSAGES = [
    "Thank you so much! Your leaflet has been added to the archive.",
    "Thanks, that's one more towards the target!",
    "Great! Thank you!",
    "Thanks for the leaflet, the election is a tiny bit more transparent!",
]

REPORT_EMAIL_SUBJECT = "Leaflet Report"

TEST_RUNNER = "django.test.runner.DiscoverRunner"

DEVS_DC_AUTH_TOKEN = environ.get("DEVS_DC_AUTH_TOKEN", None)
YNR_API_KEY = None
YNR_BASE_URL = "https://candidates.democracyclub.org.uk"

if "testing" not in environ.get("DJANGO_SETTINGS_MODULE", ""):
    # .local.py overrides all the common settings.
    try:
        from .local import *  # noqa: F401,F403

        INTERNAL_IPS = [
            "127.0.0.1",
        ]
    except ImportError:
        pass
