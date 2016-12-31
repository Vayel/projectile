import os

from .document_uploader import DocumentUploader


class DriveDocumentUploader(DocumentUploader):
    def __init__(self, root_dirname, validated_dirname, drive, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.drive = drive
        self.root_dirname = root_dirname
        self.validated_dirname = validated_dirname
 
 
    def create_folder(self, doc_names):
        self.root_id = self.drive.create_folder(self.root_dirname, [])

        # Create folder for each document
        for doc in doc_names:
            folder_name = os.path.splitext(doc)[0]
            folder_id = self.drive.create_folder(folder_name, [self.root_id])
            self.drive.create_folder(self.validated_dirname, [folder_id])


    def share_folder(self, mail):
        self.drive.share_file(self.root_id, mail)
