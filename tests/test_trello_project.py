import os

import pytest
from conftest import HERE

from projectile.project import TrelloProject, NoProjectManagerError
from projectile.tools import Trello


TRELLO_APP_SECRET_PATH = os.path.join(HERE, 'trello_api_secret.txt')
DESIGN_LIST_ID = '57c165e20c6633f204363000'
QUALITY_MEMBER_CARD_URL = 'https://trello.com/c/OJ69t7ch/35-qualiteux'
QUALITY_CHIEF_CARD_URL = 'https://trello.com/c/u7J7bL03/34-chef-qualiteux'


@pytest.fixture(scope="module")
def trello():
    if os.path.isfile(TRELLO_APP_SECRET_PATH):
        os.unlink(TRELLO_APP_SECRET_PATH)
 
    return Trello(
        os.environ['TRELLO_API_KEY'],
        TRELLO_APP_SECRET_PATH,
        'Projectile - Nsigma (test)'
    )


def create_project(url, trello, path=HERE):
    return TrelloProject(
        url,
        trello,
        design_list_id=DESIGN_LIST_ID,
        quality_member_card_url=QUALITY_MEMBER_CARD_URL,
        quality_chief_card_url=QUALITY_CHIEF_CARD_URL,
        path=path,
        output_dirname='pdf',
    )


def test_create_project(project_folder, trello):
    p = create_project('https://trello.com/c/HJvMyd72/31-sdqsqd', trello, project_folder)
    p.create_folder()


def test_is_project_manager_on_card(trello):
    p = create_project('https://trello.com/c/mYdS4kuB/32-avec-chaff', trello)
    assert p.is_project_manager_on_card()
    
    p = create_project('https://trello.com/c/sgTFUpd1/33-sans-chaff', trello)
    assert not p.is_project_manager_on_card()


def test_get_quality_member_id_with_quality_member(trello):
    p = create_project('https://trello.com/c/0fAaRvtW/36-avec-qualiteux', trello)
    assert p.get_quality_member_id() == '564c8e66ef84df030c4ee784'
    

def test_get_quality_member_id_without_quality_member(trello):
    p = create_project('https://trello.com/c/QgD28Df2/37-sans-qualiteux', trello)
    assert p.get_quality_member_id() == '57b6d799e8e1bdca314d5ea5'


def test_design_with_project_manager(trello):
    p = create_project('https://trello.com/c/8pu0EOKz/38-ap-avec-chaff', trello)
    p.design()

    p.read_card()

    assert p.card['idList'] == DESIGN_LIST_ID


def test_design_without_project_manager(trello):
    p = create_project('https://trello.com/c/lIBWZeHk/39-ap-sans-chaff', trello)
    with pytest.raises(NoProjectManagerError):
        p.design()
