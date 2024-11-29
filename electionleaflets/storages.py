import abc
from pathlib import Path
from urllib.parse import urlsplit, unquote, urlunsplit

from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.core.files.storage import FileSystemStorage, default_storage
from pipeline.storage import PipelineMixin
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(PipelineMixin, ManifestStaticFilesStorage):
    manifest_strict = False

    def stored_name(self, name):
        """
        If the file doesn't exist, just return the name given
        rather than blowing up with a 500.

        This is something that I consider to be a bug in Django.

        This issue for it is here: https://code.djangoproject.com/ticket/31520
        """
        parsed_name = urlsplit(unquote(name))
        clean_name = parsed_name.path.strip()
        hash_key = self.hash_key(clean_name)
        cache_name = self.hashed_files.get(hash_key)

        # ---
        # This bit is changed from the parent class
        if cache_name is None and not self.manifest_strict:
            return name
        # ---

        unparsed_name = list(parsed_name)
        unparsed_name[2] = cache_name
        # Special casing for a @font-face hack, like url(myfont.eot?#iefix")
        # http://www.fontspring.com/blog/the-new-bulletproof-font-face-syntax
        if "?#" in name and not unparsed_name[3]:
            unparsed_name[2] += "?"
        return urlunsplit(unparsed_name)


class TempUploadBaseMixin(abc.ABC):
    """
    This is a placeholder class that does nothing,
    but other media classes will inherit from.

    The point of this class is to give us something to assert against:
    Leaflet uploads require a sub-class of this class to be in use, so we can
    raise errors if someone attempts to use a storage class that doesn't
    implement `save_from_temp_upload`.

    """

    @abc.abstractmethod
    def save_from_temp_upload(self, source_path, target_file_path):
        ...


class TempUploadS3MediaStorage(TempUploadBaseMixin, S3Boto3Storage):
    def save_from_temp_upload(self, source_path, target_file_path):
        self.copy_file(source_path, target_file_path)

    def copy_file(self, source_path, target_file_path):
        copy_source = {
            "Bucket": self.bucket.name,
            "Key": source_path,
        }
        moved_file = self.bucket.Object(str(target_file_path))
        moved_file.copy(copy_source)
        return moved_file

class TempUploadLocalMediaStorage(TempUploadBaseMixin, FileSystemStorage):
    def save_from_temp_upload(self, source_path, target_file_path: Path):
        target_file_path = Path(default_storage.path(target_file_path))
        target_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(default_storage.path(source_path), "rb") as source_file:
            with target_file_path.open("wb") as dest_file:
                dest_file.write(source_file.read())
