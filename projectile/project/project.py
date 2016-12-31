import os

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


    def __init__(self, name, path, output_dirname, reader=None, downloader=None, uploader=None, state='', document_dirname='documents'):
        self.name = name
        self.slug = slugify(self.name)
        self.path = os.path.join(path, self.slug)
        self.reader = reader
        self.downloader = downloader
        self.uploader = uploader
        self.state = state or Project.DESIGNED
        self.document_dirname = document_dirname
        self.output_dirname = output_dirname


    def get_document_path(self, fname=''):
        return os.path.join(self.path, self.document_dirname, fname)


    def get_output_path(self, fname=''):
        return os.path.join(self.get_document_path(), self.output_dirname, fname) 


    def create_folder(self):
        try:
            os.makedirs(self.get_output_path())
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
