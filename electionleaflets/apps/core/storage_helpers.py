from formtools.wizard.storage.session import SessionStorage


class PreUploadedSessionStorage(SessionStorage):
    def reset(self):
        # Store unused temporary file names in order to delete them
        # at the end of the response cycle through a callback attached in
        # `update_response`.
        wizard_files = self.data[self.step_files_key]
        for step_files in wizard_files.values():
            for file_list in step_files.values():
                for step_file in file_list:
                    self._tmp_files.append(step_file["tmp_name"])
        self.init_data()

    def set_step_files(self, step, files):
        return
