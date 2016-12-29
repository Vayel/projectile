import os

from slugify import slugify

import pytest
from conftest import HERE, PROJECT_FOLDER

from odf.opendocument import OpenDocumentText, OpenDocumentSpreadsheet

from projectile import LibreOfficeProject, NoODSFile


ODS_NAME = 'myods'


def fill_folder(folder, with_ods=True):
    OpenDocumentText().save(os.path.join(folder, 'doc'), True)
    if with_ods:
        OpenDocumentSpreadsheet().save(os.path.join(folder, ODS_NAME), True)


def test_create_project(project_folder):
    p = LibreOfficeProject('1', PROJECT_FOLDER)
    p.create_folder()


def test_open_document(project_folder):
    p = LibreOfficeProject('1', PROJECT_FOLDER)
    p.create_folder()
    fill_folder(str(p.get_document_path()))
    p.open_document('doc.odt')


def test_get_ods_name_with_ods(project_folder):
    p = LibreOfficeProject('1', PROJECT_FOLDER)
    p.create_folder()
    fill_folder(str(p.get_document_path()))
    
    assert p.get_ods_name() == ODS_NAME
    
    
def test_get_ods_name_without_ods(project_folder):
    p = LibreOfficeProject('1', PROJECT_FOLDER)
    p.create_folder()
    fill_folder(str(p.get_document_path()), with_ods=False)
    
    with pytest.raises(NoODSFile):
        p.get_ods_name()


def test_setup(project_folder):
    name = 'Mon projet'
    p = LibreOfficeProject(name, PROJECT_FOLDER)
    p.create_folder()
    fill_folder(str(p.get_document_path()))

    p.setup()
    assert os.path.isfile(str(p.get_document_path(fname=slugify(name) + '.ods')))
