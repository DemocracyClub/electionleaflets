from urllib.parse import urlsplit, unquote, urlunsplit

from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from pipeline.storage import PipelineMixin


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
