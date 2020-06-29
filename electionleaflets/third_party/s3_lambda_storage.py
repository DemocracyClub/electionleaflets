import os

from django.conf import settings
from django.contrib.staticfiles.storage import ManifestFilesMixin
from pipeline.storage import PipelineMixin
from storages.backends.s3boto3 import S3Boto3Storage, SpooledTemporaryFile


class S3StaticStorage(PipelineMixin, ManifestFilesMixin, S3Boto3Storage):
    manifest_strict = False
    manifest_name = settings.STATICFILES_MANIFEST_NAME

    def __init__(self, *args, **kwargs):
        kwargs["location"] = settings.STATIC_URL
        super(S3StaticStorage, self).__init__(*args, **kwargs)

    # Temporary fix for https://github.com/jschneier/django-storages/issues/382
    # Without this, collectstatic errors when uploading to S3 because it's not
    # rewinding the `StreamingBody`
    def _save_content(self, obj, content, parameters):
        """
        We create a clone of the content file as when this is passed to boto3 it wrongly closes
        the file upon upload where as the storage backend expects it to still be open
        """
        # Seek our content back to the start
        content.seek(0, os.SEEK_SET)

        # Create a temporary file that will write to disk after a specified size
        content_autoclose = SpooledTemporaryFile()

        # Write our original content into our copy that will be closed by boto3
        content_autoclose.write(content.read())

        # Upload the object which will auto close the content_autoclose instance
        super(S3StaticStorage, self)._save_content(
            obj, content_autoclose, parameters
        )

        # Cleanup if this is fixed upstream our duplicate should always close
        if not content_autoclose.closed:
            content_autoclose.close()
