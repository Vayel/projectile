import os
from subprocess import call

from .document_reader import DocumentReader


class NoODSFile(FileNotFoundError): pass


class LibreOfficeDocumentReader(DocumentReader):
    def __init__(self, db_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_name = db_name


    def read_document(self, fname):
        call(['libreoffice', self.get_document_path(fname)])
 
    
    def get_ods_name(self):
        try:
            return [f for f in self.get_document_fnames() if f.endswith('.ods')][0][:-4]
        except IndexError:
            raise NoODSFile('Le projet ne comporte pas de fichier .ods.')
    
    
    def configure_documents(self):
        # Rename the .ods file to obtain explicit database names
        os.rename(
            self.get_document_path(self.get_ods_name() + '.ods'),
            self.get_document_path(self.db_name + '.ods')
        )
