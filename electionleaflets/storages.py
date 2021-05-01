from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from pipeline.storage import PipelineMixin


class StaticStorage(PipelineMixin, ManifestStaticFilesStorage):
    pass
