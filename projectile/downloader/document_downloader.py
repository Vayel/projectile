from .. import DocumentManager


class DocumentDownloader(DocumentManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
    def download_documents(self):
        raise NotImplementedError()
