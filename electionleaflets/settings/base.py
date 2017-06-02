import sys
from os.path import join, abspath, dirname
from os import environ

# PATH vars
here = lambda *x: join(abspath(dirname(__file__)), *x)
PROJECT_ROOT = here("..")
root = lambda *x: join(abspath(PROJECT_ROOT), *x)
sys.path.insert(0, root('third_party'))
sys.path.insert(0, root('apps'))
sys.path.insert(0, '../django-uk-political-parties/')


DEBUG = False
template_DEBUG = DEBUG

# DATABASES define in environment specific settings file
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'electionleaflets',
        'USER': 'electionleaflets',
    }
}


TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-GB'

ALLOWED_HOSTS = []

MEDIA_ROOT = root('media', )
MEDIA_URL = '/media/'
STATIC_ROOT = root('static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    root('media'),
)

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_FILE_OVERWRITE = False

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SITE_ID=1
USE_I18N = False
USE_L10N = True
LOGIN_URL = "/"

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Don't share this with anybody.
SECRET_KEY = "elyfryi8on!dmw&8b3j-g0yve4u&%4_6%(tf3*)@#&mq*$yzhf^6"

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'leaflets.middleware.SourceTagMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'linaro_django_pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'electionleaflets.urls'
WSGI_APPLICATION = 'electionleaflets.wsgi.application'

LEAFLET_APPS = [
    'core',
    'leaflets',
    'parties',
    'constituencies',
    'analysis',
    'categories',
    'tags',
    'content',
    'elections',
    'people',
]

INSTALLED_APPS = [
    'celery',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.humanize',
    'kombu.transport.django',
    'linaro_django_pagination',
    'rest_framework',
    'sorl.thumbnail',
    'storages',
    'uk_political_parties',
    'markdown_deux',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'django_extensions',
] + LEAFLET_APPS

if environ.get('SENTRY_DSN', None):
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')
    RAVEN_CONFIG = {
        'dsn': environ.get('SENTRY_DSN'),
        'environment': environ.get('SENTRY_ENVIRONMENT', 'production')
    }


THUMBNAIL_FORMAT = 'PNG'
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                'django.template.context_processors.request',
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.contrib.auth.context_processors.auth",
            ]
        }
    }
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

SOCIALACCOUNT_PROVIDERS = {
    'google': {'SCOPE': ['https://www.googleapis.com/auth/userinfo.profile'],
               'AUTH_PARAMS': {'access_type': 'online'}},
    'facebook': {'SCOPE': ['email',]},
}

LOGIN_REDIRECT_URL = '/'

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
SOCIALACCOUNT_AUTO_SIGNUP = True

THANKYOU_MESSAGES = [
    'Thank you so much! Your leaflet has been added to the archive.',
    'Thanks, that\'s one more towards the target!',
    'Great! Thank you!',
    'Thanks for the leaflet, the election is a tiny bit more transparent!'
    ]

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

MAPIT_API_KEY = environ.get('MAPIT_API_KEY', None)
MAPIT_API_URL = environ.get('MAPIT_API_URL', 'https://mapit.democracyclub.org.uk/')

# .local.py overrides all the common settings.
try:
    from .local import *
except ImportError:
    pass


# importing test settings file if necessary (TODO chould be done better)
if len(sys.argv) > 1 and sys.argv[1] in ['test', 'harvest']:
    try:
        from .testing import *
    except ImportError:
        pass

