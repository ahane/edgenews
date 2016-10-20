# -*- coding: utf-8 -*-
import pytest

from edgenews.api import serialize

@pytest.fixture
def new_user_jsonapi():

    return {'data':
                {'type': 'user',
                 'attributes':
                     {'name': 'bert',
                     'email': 'some@email.com',
                     'plain_password': 'abc'}}}


@pytest.fixture
def empty_new_user_jsonapi():

    return {}


@pytest.fixture
def empty_new_user_response():

    return {'errors': ['Object must include `data` key.']}


@pytest.fixture
def corrupt_new_user_jsonapi():

    return {'data':
                {'type': 'user',
                 'attributes':
                     {'name': '',
                      'emaisl': 'some@email.com',
                      'plain_password': 'abc'}}}


@pytest.fixture
def corrupt_new_user_response():

    return {'errors': [
                {'detail': 'Missing data for required field.',
                'source': {'pointer': '/data/attributes/email'},
                'status': '400',
                'title': 'Validation Error'},

                {'detail': 'Length must be between 1 and 255.',
                'source': {'pointer': '/data/attributes/name'},
                'status': '400',
                'title': 'Validation Error'}]}


@pytest.fixture
def new_user():

    return {'name': 'bert',
            'email': 'some@email.com',
            'plain_password': 'abc'}


def test_deserialize_new_user(new_user_jsonapi, new_user):
    actual = serialize.deserialize_user(new_user_jsonapi)
    expected = new_user
    assert actual == expected


def test_deserialize_empty_new_user(empty_new_user_jsonapi,
                                    empty_new_user_response):

    with pytest.raises(serialize.ValidationError) as err:
        serialize.deserialize_user(empty_new_user_jsonapi)

    assert 'errors' in err.value.messages


def test_deserialize_currupt_new_user(corrupt_new_user_jsonapi,
                                      corrupt_new_user_response):

    with pytest.raises(serialize.ValidationError) as err:
        serialize.deserialize_user(corrupt_new_user_jsonapi)

    assert 'errors' in err.value.messages


def test_get_status_code_200(new_user_jsonapi):

    actual = serialize.get_status_code(new_user_jsonapi)
    expected = 200

    assert actual == expected


def test_get_status_code_200(new_user_jsonapi):

    actual = serialize._get_status_code(new_user_jsonapi)
    expected = 200

    assert actual == expected


def test_get_status_code_error(corrupt_new_user_response):

    actual = serialize._get_status_code(corrupt_new_user_response)
    expected = 400

    assert actual == expected

def test_add_status_code_decorator(corrupt_new_user_response):

    @serialize.add_status_code
    def some_func():
        return corrupt_new_user_response

    actual = some_func()
    expected = (corrupt_new_user_response, 400)

    assert actual == expected