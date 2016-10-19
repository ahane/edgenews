# -*- coding: utf-8 -*-
import pytest

from edgenews import core
@pytest.fixture
def some_new_user():
    return {'name': 'bert', 'email': 'a@example.com', 'plain_password': 'abc'}

@pytest.fixture
def corrupt_new_users():
    return [{'name': 'bert', 'email': 'a@example.com'},
        {'name': 'bert'},
        {'name': 'bert', 'email': 'bert', 'plain_password': 'abc'},
        {'name': '', 'email': 'a@example.com', 'plain_password': 'abc'}]





@pytest.fixture
def prepared_user(some_new_user):
    return core.user.init(some_new_user)

@pytest.mark.core
def test_is_valid(some_new_user):
    assert core.user.is_valid_new_user(some_new_user)

@pytest.mark.core
def test_is_valid_fail(corrupt_new_users):
    for user in corrupt_new_users:
        assert not core.user.is_valid_new_user(user)

@pytest.mark.core
def test_user_prepared(prepared_user):
    print(prepared_user)
    assert core.user.is_valid(prepared_user)
