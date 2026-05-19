import os
import shutil

class FileUploadService:

    def __init__(self, upload_dir: str, event_manager):

        self.upload_dir = upload_dir
        self.event_manager = event_manager

        os.makedirs(upload_dir, exist_ok=True)

    async def upload(self, file):

        file_path = os.path.join(
            self.upload_dir,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        self.event_manager.notify(
            "file_uploaded",
            {
                "filename": file.filename,
                "path": file_path
            }
        )

        return {
            "message": "Archivo subido correctamente",
            "filename": file.filename
        }