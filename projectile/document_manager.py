import os


class DocumentManager:
    def __init__(self, path):
        self.path = path


    def get_document_path(self, fname=''):
        return os.path.join(self.path, fname)


    def get_document_fnames(self):
        return [f for f in os.listdir(self.path) if os.path.isfile(self.get_document_path(f))]
