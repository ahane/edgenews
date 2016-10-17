# -*- coding: utf-8 -*-
import pytest

from edgenews import core

@pytest.fixture
def some_new_user():
    return {'name': 'bert', 'email': 'a@example.com', 'plain_password': 'abc'}

@pytest.fixture
def corrupt_new_users():
    return [{'name': 'bert', 'email': 'a@example.com', 'shouldntbeher': True, 'plain_password': 'abc'},
            {'name': 'bert', 'email': 'a@example.com'},
            {'name': 'bert'},
            {'name': 'bert', 'email': 'bert', 'plain_password': 'abc'},
            {'name': '', 'email': '', 'plain_password': 'abc'}]

@pytest.fixture
def prepared_user(some_new_user):
    return core.prepare_user(some_new_user)

def test_is_valid_user(some_new_user):
    assert core.is_valid_new_user(some_new_user)

def test_is_valid_user_fail(corrupt_new_users):
    for user in corrupt_new_users:
        assert not core.is_valid_new_user(user)

def test_user_prepared(prepared_user):
    print(prepared_user)
    assert core.is_valid_user(prepared_user)
