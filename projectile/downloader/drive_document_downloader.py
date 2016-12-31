import os

from .document_downloader import DocumentDownloader


class DriveDocumentDownloader(DocumentDownloader):
    def __init__(self, drive, folder_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.drive = drive
        self.query = "'{}' in parents and not trashed".format(folder_id)
        
    
    def download_documents(self):
        documents = self.drive.list_files(self.query)
        
        for document in documents:
            save_path = self.get_document_path(document['name'])
            self.drive.download_file(document['id'], save_path)
