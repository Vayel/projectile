import os

import pytest

from projectile.project import Project, ProjectExistsError


def test_create_project(project_folder):
    p1 = Project('1', project_folder, 'pdf')
    p2 = Project('2', project_folder, 'pdf')
    p1_ = Project('1', project_folder, 'pdf')


def test_create_folder(project_folder):
    Project('1', project_folder, 'pdf').create_folder()
    assert os.path.exists(os.path.join(project_folder, '1'))

    Project('2', project_folder, 'pdf').create_folder()
    assert os.path.exists(os.path.join(project_folder, '2'))

    with pytest.raises(ProjectExistsError):
        Project('1', project_folder, 'pdf').create_folder()
