import uuid

import pytest

from edgenews import interact
from edgenews import store
from .test_core import some_new_user

@pytest.fixture(scope='module')
def register_repos():
    store.Registry.register('user', store.MemoryRepository('user'))

@pytest.fixture(scope='module')
def user_store(register_repos):
    return store.Registry.get_repo('user')

@pytest.fixture(scope='module')
def some_uuid4():
    return uuid.UUID('7cc94b14-fcdd-4c08-a41a-080cd4596bfb')

@pytest.fixture(scope='module')
def monkeypatch_uuid4(request, some_uuid4):
    old = uuid.uuid4
    uuid.uuid4 = lambda : some_uuid4
    def fin():
        uuid.uuid4 = old
    request.addfinalizer(fin)

@pytest.fixture
def created_user(some_uuid4):
    return {'is_anonymous': False,
            'salt': some_uuid4.hex,
            '_id': 0,
            'email': 'a@example.com',
            'name': 'bert',
            'hashed_password': 'b6f9e0c4c3b8c7ba96afd4c1bd76f52f84dea0a566f811f8a10d2bdfbc637bbf',
            'is_active': True}


def test_create_user(some_new_user, user_store, monkeypatch_uuid4):

    user, msg = interact.UserManager().create_user(some_new_user)
    assert msg == 'ok'
    assert len(user_store._records) == 1

def test_get_user(some_new_user, created_user):
    user, msg = interact.UserManager().get_user(some_new_user['name'])
    assert user == created_user
    assert msg == 'ok'

def test_get_user_fail():
    user, msg = interact.UserManager().get_user('idonotexist')
    assert user is None
    assert msg == 'no user found with name=idonotexist'

def test_list_users(some_new_user, user_store):
    users, msg = interact.UserManager().list_users()
    assert len(user_store._records) == 1
    assert len(users) == 1
    assert msg == 'ok'

def test_create_user_fail(some_new_user, user_store):

    user, msg = interact.UserManager().create_user(some_new_user)
    assert user is None
    assert msg == 'username already taken'
    assert len(user_store._records) == 1


# def test_authenticate(some_new_user, user_store):
#     name, pwd = some_new_user['name'], some_new_user['plain_password']
#     user, msg = interact.UserManager().authenticate(name, pwd)
#     assert user
#     assert msg == 'ok'
#
#
# def test_authenticate_fail(some_new_user, user_store):
#     name, pwd = some_new_user['name'], 'wrongpassword'
#     user, msg = interact.UserManager().authenticate(name, pwd)
#     assert user == None
#     assert msg == 'could not authenticate'
