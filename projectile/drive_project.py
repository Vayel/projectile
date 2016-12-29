from .project import Project
from .tools import Drive

__all__ = ('DriveProject',)


class DriveProject(Project):
    def __init__(self, name, folder, user_drive, app_drive, template_drive_id, pdf_dirname='pdf', validated_dirname='validated'):
        self.user_drive = user_drive
        self.app_drive = app_drive
        self.template_drive_id = template_drive_id
        self.pdf_dirname = pdf_dirname
        self.validated_dirname = validated_dirname

        super().__init__(name, folder)


    def download_documents(self):
        documents = self.app_drive.list_files("'{}' in parents and not trashed".format(self.template_drive_id))
        
        for document in documents:
            save_path = str(self.get_document_path(fname=document['name']))
            self.app_drive.download_file(document['id'], save_path)
    
    
    def create_drive_folder(self):
        self.root_id = self.user_drive.create_folder(self.name, [])
        pdf_id = self.user_drive.create_folder(self.pdf_dirname, [self.root_id])

        # Create folder for each document
        for doc in self.get_document_names():
            folder_id = self.user_drive.create_folder(doc, [pdf_id])
            self.user_drive.create_folder(self.validated_dirname, [folder_id])


    def share_folder(self, mail):
        self.user_drive.share_file(self.root_id, mail)
