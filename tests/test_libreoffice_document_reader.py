import os

import pytest

from odf.opendocument import OpenDocumentText, OpenDocumentSpreadsheet

from projectile.reader import LibreOfficeDocumentReader, NoODSFile


ODS_NAME = 'myods'
DB_NAME = 'mydb'


def fill_folder(folder, with_ods=True):
    OpenDocumentText().save(os.path.join(folder, 'doc'), True)
    if with_ods:
        OpenDocumentSpreadsheet().save(os.path.join(folder, ODS_NAME), True)


def test_init(document_folder):
    LibreOfficeDocumentReader(DB_NAME, document_folder)


def test_read_document(document_folder):
    r = LibreOfficeDocumentReader(DB_NAME, document_folder)
    fill_folder(r.path)
    r.read_document('doc.odt')


def test_get_ods_name_with_ods(document_folder):
    r = LibreOfficeDocumentReader(DB_NAME, document_folder)
    fill_folder(r.path)
    
    assert r.get_ods_name() == ODS_NAME
    
    
def test_get_ods_name_without_ods(document_folder):
    r = LibreOfficeDocumentReader(DB_NAME, document_folder)
    fill_folder(r.path, with_ods=False)
    
    with pytest.raises(NoODSFile):
        r.get_ods_name()


def test_configure_documents(document_folder):
    r = LibreOfficeDocumentReader(DB_NAME, document_folder)
    fill_folder(r.path)
    r.configure_documents()

    assert os.path.isfile(r.get_document_path(fname=DB_NAME + '.ods'))
