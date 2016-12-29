import os

import pytest
from conftest import PROJECT_FOLDER

from projectile import Project, ProjectExistsError


def test_create_project(emulate_project_folder):
    p1 = Project('1', PROJECT_FOLDER)
    p2 = Project('2', PROJECT_FOLDER)
    p1_ = Project('1', PROJECT_FOLDER)


def test_create_folder(emulate_project_folder):
    Project('1', PROJECT_FOLDER).create_folder()
    assert os.path.exists(os.path.join(PROJECT_FOLDER, '1'))

    Project('2', PROJECT_FOLDER).create_folder()
    assert os.path.exists(os.path.join(PROJECT_FOLDER, '2'))

    with pytest.raises(ProjectExistsError):
        Project('1', PROJECT_FOLDER).create_folder()
