from django.core.files.uploadedfile import UploadedFile
from django.utils.datastructures import MultiValueDict
from formtools.wizard.storage import NoFileStorageConfigured
from formtools.wizard.storage.session import SessionStorage
from storages.backends.s3boto3 import S3Boto3StorageFile


class PreUploadedSessionStorage(SessionStorage):
    def reset(self):
        # Store unused temporary file names in order to delete them
        # at the end of the response cycle through a callback attached in
        # `update_response`.
        wizard_files = self.data[self.step_files_key]
        for step_files in wizard_files.values():
            for file_list in step_files.values():
                for step_file in file_list:
                    self._tmp_files.append(step_file['tmp_name'])
        self.init_data()

    def set_step_files(self, step, files):
        if files and not self.file_storage:
            raise NoFileStorageConfigured(
                "You need to define 'file_storage' in your "
                "wizard view in order to handle file uploads."
            )

        if step not in self.data[self.step_files_key]:
            self.data[self.step_files_key][step] = {}

        for field, field_file in (files or {}).items():
            self.data[self.step_files_key][step][field] = []
            for s3_file in files.getlist(field):
                if isinstance(s3_file, S3Boto3StorageFile):
                    name = s3_file.obj.key
                else:
                    name = self.file_storage.save(s3_file.name, s3_file)
                file_dict = {
                    "tmp_name": name,
                    "name": s3_file.name,
                    "content_type": s3_file.obj.content_type,
                    "size": s3_file.size,
                }
                self.data[self.step_files_key][step][field].append(file_dict)

    def get_step_files(self, step):
        wizard_files = self.data[self.step_files_key].get(step, {})

        files = {}
        for field in wizard_files.keys():
            files[field] = {}
            uploaded_file_list = []

            for field_dict in wizard_files.get(field, []):
                field_dict = field_dict.copy()
                tmp_name = field_dict.pop("tmp_name")
                if (step, field, field_dict["name"]) not in self._files:
                    self._files[
                        (step, field, field_dict["name"])
                    ] = UploadedFile(
                        file=self.file_storage.open(tmp_name), **field_dict
                    )
                uploaded_file_list.append(
                    self._files[(step, field, field_dict["name"])]
                )
            files[field] = uploaded_file_list
        if files:
            return MultiValueDict(files)
        return None
