from .. import DocumentManager


class DocumentUploader(DocumentManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
    def create_destination_folder(self):
        raise NotImplementedError()


    def upload_document(self, fname):
        raise NotImplementedError()
