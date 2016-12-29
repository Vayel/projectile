import os
from pathlib import Path

from slugify import slugify

__all__ = ('ProjectExistsError', 'InvalidStateError', 'Project',)

# Exceptions
class ProjectExistsError(FileExistsError): pass
class InvalidStateError(RuntimeError): pass


class Project:
    DESIGNED = 'designed'
    DEVELOPPED = 'developped'
    ABORTED = 'aborted'
    FINISHED = 'finished'
    VALIDATED = 'validated' # By the quality section


    def __init__(self, name, path, state='', document_dirname='documents', pdf_dirname='pdf'):
        self.name = name
        self.slug = slugify(self.name)
        self.path = Path(path) / self.slug
        self.state = state or Project.DESIGNED
        self.document_dirname = document_dirname
        self.pdf_dirname = pdf_dirname


    def get_document_path(self, fname=''):
        return self.path / self.document_dirname / fname


    def get_pdf_path(self, fname=''):
        return self.get_document_path() / self.pdf_dirname / fname      


    def create_folder(self):
        try:
            os.makedirs(str(self.get_pdf_path()))
        except FileExistsError:
            raise ProjectExistsError('Un dossier de projet porte déjà ce nom.')


    def design(self):
        self.state = Project.DESIGNED


    def develop(self):
        if self.state != Project.DESIGNED:
            raise InvalidStateError()

        self.state = Project.DEVELOPPED


    def abort(self):
        if self.state not in (Project.DESIGNED, Project.DEVELOPPED):
            raise InvalidStateError()


    def finish(self):
        if self.state != Project.DEVELOPPED:
            raise InvalidStateError()


    def validate(self):
        if self.state != Project.FINISHED:
            raise InvalidStateError()
