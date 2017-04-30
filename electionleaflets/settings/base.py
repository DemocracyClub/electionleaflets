import environ, sys
root = environ.Path(__file__) - 2 # three folder back (/a/b/c/ - 3 = /)
env = environ.Env() # set default values and casting

sys.path.insert(0, root('third_party'))
sys.path.insert(0, root('apps'))
sys.path.insert(0, '../django-uk-political-parties/')

DEBUG = env.bool('DEBUG', default=False)
TEMPLATE_DEBUG = DEBUG

db_url = env('DATABASE_URL', default='postgres://postgres@localhost/electionleaflets')
db_url = db_url.replace('postgres://', 'postgis://')

DATABASES = {
    'default': env.db_url_config(db_url)
}

redis_url_env = env('REDIS_PROVIDER', default='REDIS_URL')
CACHES = {
    'default': env.cache(redis_url_env, default='redis://localhost:6379/0')
}

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-GB'

ALLOWED_HOSTS = ['*']

MEDIA_ROOT = root('media', )
MEDIA_URL = '/media/'
STATIC_ROOT = root('static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    root('media'),
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if env("AWS_STORAGE_BUCKET_NAME", default=None):
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_S3_FILE_OVERWRITE = env.bool("AWS_S3_FILE_OVERWRITE", default=False)
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_HOST = env("AWS_S3_HOST")

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='team@electionleaflets.org')
EMAIL_RECIPIENT = env('EMAIL_RECIPIENT', default='team@electionleaflets.org')
REPORT_EMAIL_SUBJECT = env('REPORT_EMAIL_SUBJECT', default='ELECTION LEAFLET REPORT')

MAINTENANCE_MODE = env.bool('MAINTENANCE_MODE', default=False)
GOOGLE_ANALYTICS_ENABLED = env.bool('GOOGLE_ANALYTICS_ENABLED', default=False)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

TWITTER_KEY = env('TWITTER_KEY', default='')
TWITTER_SECRET = env('TWITTER_SECRET', default='')
TWITTER_TOKEN = env('TWITTER_TOKEN', default='')
TWITTER_TOKEN_SECRET = env('TWITTER_TOKEN_SECRET', default='')

ADMINS = [a.split(',') for a in env('ADMINS', default='').split(';')]
MANAGERS = ADMINS

SITE_ID=1
USE_I18N = False
USE_L10N = True
LOGIN_URL = "/"

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

SECRET_KEY = env('SECRET_KEY', default='INSECURE')

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
    'aloe_django',
    'sslserver',
] + LEAFLET_APPS


THUMBNAIL_FORMAT = 'PNG'
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.cached_db_kvstore.KVStore'


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
        'rest_framework.permissions.AllowAny'
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

THEYWORKFORYOU_API_KEY = env('THEYWORKFORYOU_API_KEY', default='')


# importing test settings file if necessary (TODO chould be done better)
if len(sys.argv) > 1 and sys.argv[1] in ['test', 'harvest']:
    try:
        from .testing import *
    except ImportError:
        pass

