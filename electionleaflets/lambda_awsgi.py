import os
from os.path import abspath, dirname
from sys import path

import awsgi
from django.core.wsgi import get_wsgi_application

SITE_ROOT = dirname(dirname(abspath(__file__)))
path.append(SITE_ROOT)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "electionleaflets.settings.base_lambda")


application = get_wsgi_application()


def handler(event, context):
    return awsgi.response(
        application,
        event,
        context,
        base64_content_types={
            "image/png",
            "image/x-icon",
            "image/jpeg",
            "image/jpg",
            "font/woff2",
        },
    )