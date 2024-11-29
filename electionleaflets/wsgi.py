import os
from os.path import abspath, dirname
from sys import path

from django.core.wsgi import get_wsgi_application

SITE_ROOT = dirname(dirname(abspath(__file__)))
path.append(SITE_ROOT)


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "electionleaflets.settings.base_lambda"
)


application = get_wsgi_application()
