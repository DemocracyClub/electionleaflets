from pathlib import Path

from sorl.thumbnail import default
from sorl.thumbnail.base import ThumbnailBackend
from sorl.thumbnail.images import ImageFile


class BaseThumbsCustomUrlBackend(ThumbnailBackend):
    def _get_thumbnail_filename(self, source, geometry_string, options):
        """
        Returns URLs that match the format of the lambda@edge function
        that creates the initial thumbnails on S3. This means that we don't
        need to use the lambda instance the Django app runs on to process
        thumbnails, as they should already exist.
        """

        base_url = "thumbs"

        opts = options.copy()
        for k, v in list(opts.items()):
            if self.default_options[k] == v:
                del opts[k]

        url_kwargs = "/".join(
            ["{}={}".format(k, v) for k, v in list(opts.items())]
        )
        file_path = Path(source.name)
        file_name = file_path.parent / file_path.stem

        return "{base_url}/{geometry_string}/{url_kwargs}/{original_path}.png".format(
            base_url=base_url,
            geometry_string=geometry_string,
            url_kwargs=url_kwargs,
            original_path=file_name,
        )


class S3Backend(BaseThumbsCustomUrlBackend):
    def get_thumbnail(self, file_, geometry_string, **options):
        """
        Returns thumbnail as an ImageFile instance for file with geometry and
        options given. All of the thumbnail generation logic is short-circuited
        as we know that CloudFront will generate the thumbnail for us.
        """
        if file_:
            source = ImageFile(file_)
        else:
            return None

        for key, value in list(self.default_options.items()):
            options.setdefault(key, value)

        name = self._get_thumbnail_filename(source, geometry_string, options)
        return ImageFile(name, default.storage)


class LocalThumbnailBackend(BaseThumbsCustomUrlBackend): ...
