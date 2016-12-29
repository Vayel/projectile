import os

from slugify import slugify

import pytest
from conftest import HERE, PROJECT_FOLDER

from projectile import DriveProject
from projectile.tools import Drive


def drive(prefix):
    credentials_path = os.path.join(HERE, prefix + '_google_credentials.json')

    try:
        os.remove(credentials_path)
    except FileNotFoundError:
        pass

    return Drive(
        api_key_path=os.path.join(HERE, 'google_api_key.json'),
        credentials_path=credentials_path ,
        scopes='https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.readonly',
        app_name='Projectile - Nsigma ({})'.format(prefix),
    )

@pytest.fixture(scope="module")
def user_drive():
    return drive('user')


@pytest.fixture(scope="module")
def app_drive():
    return drive('app')


def create_project(name, user_drive, app_drive):
    return DriveProject(
        name,
        PROJECT_FOLDER,
        user_drive,
        app_drive,
        template_drive_id='0B40zKDFmo_14d3B3WDJDclJtcGs',
    )


def test_create_project(user_drive, app_drive):
    create_project('test-project-1', user_drive, app_drive) 


def test_download_documents(project_folder, user_drive, app_drive):
    p = create_project('test-project-21', user_drive, app_drive) 
    p.create_folder()
    p.download_documents()


def test_create_drive_folder(project_folder, user_drive, app_drive):
    p = create_project('test-project-3', user_drive, app_drive) 
    p.create_folder()

    folder = p.get_document_path()
    open(str(folder / 'file1'), 'w').close()
    open(str(folder / 'file2'), 'w').close()

    p.create_drive_folder()


def test_share_folder(project_folder, user_drive, app_drive):
    p = create_project('test-project-4', user_drive, app_drive) 
    p.create_folder()
    p.create_drive_folder()
    p.share_folder(os.environ['TEST_DRIVE_SHARED_TO_MAIL'])
