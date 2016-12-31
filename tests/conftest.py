import os
import shutil
import pytest

from projectile.tools import Drive


HERE = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
PROJECT_FOLDER = os.path.join(HERE, 'projects')
DOCUMENT_FOLDER = os.path.join(HERE, 'documents')


def folder_fixture(path):
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass

    os.mkdir(path)

    return path


@pytest.fixture()
def project_folder():
    return folder_fixture(PROJECT_FOLDER)


@pytest.fixture()
def document_folder():
    return folder_fixture(DOCUMENT_FOLDER)


@pytest.fixture(scope="module")
def drive():
    credentials_path = os.path.join(HERE, 'google_credentials.json')

    try:
        os.remove(credentials_path)
    except FileNotFoundError:
        pass

    return Drive(
        api_key_path=os.path.join(HERE, 'google_api_key.json'),
        credentials_path=credentials_path ,
        scopes='https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.readonly',
        app_name='Projectile - Nsigma (test)',
    )
