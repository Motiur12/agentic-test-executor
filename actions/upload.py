from pathlib import Path

from .base import BaseAction


class UploadAction(BaseAction):

    def execute(
        self,
        page,
        target=None,
        value=None,
        **kwargs
    ):

        if value is None:
            raise Exception("No file specified.")

        file_path = Path(value).resolve()

        if not file_path.exists():
            raise Exception(
                f"File not found: {file_path}"
            )

        page.locator("input[type='file']").set_input_files(
            str(file_path)
        )

        print(f"✓ Uploaded '{file_path.name}'")