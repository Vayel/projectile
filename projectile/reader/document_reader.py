from .. import DocumentManager


class DocumentReader(DocumentManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def read_document(self, fname):
        raise NotImplementedError()


    def configure_documents(self):
        raise NotImplementedError()
