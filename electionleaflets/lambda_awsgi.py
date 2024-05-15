import awsgi
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


def lambda_handler(event, context):
    return awsgi.response(
        application,
        event,
        context,
        base64_content_types={
            "image/png",
            "image/jpeg",
            "image/x-icon",
            "font/woff2",
        },
    )
