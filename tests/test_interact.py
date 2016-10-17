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

def test_create_user(some_new_user, user_store):

    user, msg = interact.UserManager().create_user(some_new_user)
    assert msg == 'ok'
    assert len(user_store._records) == 1

def test_get_user():
    user, msg = interact.UserManager().get_user('idonotexist')
    assert user is None
    assert msg == 'no user found with name=idonotexist'

def test_create_user_fail(some_new_user, user_store):

    user, msg = interact.UserManager().create_user(some_new_user)
    assert user is None
    assert msg == 'username already taken'
    assert len(user_store._records) == 1


def test_authenticate_user(some_new_user, user_store):
    name, pwd = some_new_user['name'], some_new_user['plain_password']
    user, msg = interact.UserManager().authenticate_user(name, pwd)
    assert user
    assert msg == 'ok'


def test_authenticate_user_fail(some_new_user, user_store):
    name, pwd = some_new_user['name'], 'wrongpassword'
    user, msg = interact.UserManager().authenticate_user(name, pwd)
    assert user == None
    assert msg == 'could not authenticate'

def test_list_users(some_new_user, user_store):
    users, msg = interact.UserManager().list_users()
    assert len(user_store._records) == 1
    assert len(users) == 1
    assert msg == 'ok'
