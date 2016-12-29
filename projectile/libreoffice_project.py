import os
from subprocess import call

import javelot.config

from .project import Project

__all__ = ('NoODSFile', 'LibreOfficeProject',)


class NoODSFile(FileNotFoundError): pass


class LibreOfficeProject(Project):
    def __init__(self, *args, **kwargs):
        if kwargs.get('pdf_dirname') is None:
            kwargs['pdf_dirname'] = javelot.config.PDF_DIRNAME
 
        super().__init__(*args, **kwargs)


    def open_document(self, fname):
        path = str(self.get_document_path(fname))
        call(['libreoffice', path])


    def get_ods_name(self):
        folder = str(self.get_document_path())
        try:
            return [fname for fname in os.listdir(folder) if fname.endswith('.ods')][0][:-4]
        except IndexError:
            raise NoODSFile('Le projet ne comporte pas de fichier .ods.')


    def setup(self):
        # Rename the .ods file to obtain explicit database names
        os.rename(
            str(self.get_document_path(fname=self.get_ods_name() + '.ods')),
            str(self.get_document_path(fname=self.slug + '.ods'))
        )
