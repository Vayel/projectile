import os
import shutil
import pytest


HERE = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
PROJECT_FOLDER = os.path.join(HERE, 'projects')


@pytest.fixture()
def emulate_project_folder():
    try:
        shutil.rmtree(PROJECT_FOLDER)
    except FileNotFoundError:
        pass

    os.mkdir(PROJECT_FOLDER)
