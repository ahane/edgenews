# -*- coding: utf-8 -*-
import json

import pytest
import requests


def _record_to_jsonapi(record, type_):
    """helper function to quickly turn a dict to a jsonapi string"""
    wrapped = {'data': {'type': type_, 'attributes': record}}
    string = json.dumps(wrapped)

    return string


@pytest.fixture
def hostname():

    return 'localhost'


@pytest.fixture
def port():

    return '5000'


@pytest.fixture
def apiversion():

    return 'v1'


@pytest.fixture
def url(hostname, port):

    return'http://{}:{}'.format(hostname, port)


@pytest.fixture
def endpoint(apiversion):

    return '/api/{}'.format(apiversion)


@pytest.fixture
def users_endpoint(endpoint):

    return '{}/{}'.format(endpoint, 'users')


@pytest.fixture
def some_user_endpoint(users_endpoint):

    return '{}/{}'.format(users_endpoint, 'bert')

@pytest.fixture
def endpoint_response(users_endpoint):

    return {'links': {'users': users_endpoint}}


@pytest.fixture
def user_empty_response(users_endpoint):

    return {'data': [], 'links': {'self': users_endpoint}}


@pytest.fixture
def headers():

    return {'Content-Type': 'application/json'}


@pytest.fixture
def some_new_user_json():

    user = {'name': 'bert', 'email': 'a@example.com', 'plain_password': 'abc'}
    user_json = _record_to_jsonapi(user, 'user')

    return user_json


@pytest.fixture
def new_user_same_email_json():

    user = {'name': 'ernie', 'email': 'a@example.com', 'plain_password': 'abc'}
    user_json = _record_to_jsonapi(user, 'user')

    return user_json


@pytest.fixture
def corrupt_new_user():
    user = {'name': 'ernie', 'emails': 'a@example.com', 'plain_password': ''}
    user_json = _record_to_jsonapi(user, 'user')

    return user_json


@pytest.fixture
def some_new_user_response(users_endpoint):

    return {'links': {'self': '/api/v1/users/bert'},
            'data': {
                'type': 'user',
                'id': 'bert',
                'links': {'self': '/api/v1/users/bert'},
                'attributes': {'name': 'bert', 'email': 'a@example.com'}}}


@pytest.fixture
def all_users_response(users_endpoint):

    return {'links': {'self': '/api/v1/users'},
            'data': [
                {'type': 'user',
                 'id': 'bert',
                 'links': {'self': '/api/v1/users/bert'},
                 'attributes': {'name': 'bert', 'email': 'a@example.com'}}]}


@pytest.fixture
def username_conflict_response():

    return {'errors': [
                {'status': '409',
                 'title': 'User Already Exists',
                 'detail': 'username already taken'}]}


@pytest.fixture
def useremail_conflict_response():

    return {'errors': [
                {'status': '409',
                 'title': 'User Already Exists',
                 'detail': 'email address already in use'}]}


@pytest.fixture
def corrupt_new_user_conflict_response():

    return {'errors': [
                {'status': '400',
                 'title': 'Validation Error',
                 'detail': 'Missing data for required field.',
                 'source': {'pointer': '/data/attributes/email'}},
                {'status': '400',
                 'title': 'Validation Error',
                 'detail': 'Length must be between 1 and 255.',
                 'source': {'pointer': '/data/attributes/plain_password'}}]}


@pytest.mark.integration
@pytest.mark.api
def test_api_start(url, endpoint, endpoint_response):
    response = requests.get(url + endpoint).json()

    actual = response
    expected = endpoint_response

    assert actual == expected
    assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.api
def test_users_empty(url, users_endpoint, users_empty_response):
    response = requests.get(url + users_endpoint)

    actual = response.json()
    expected = users_empty_response

    assert actual == expected
    assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.api
def test_create_user(url, users_endpoint,
                     some_new_user_json,
                     some_new_user_response,
                     headers):

    response = requests.post(url + users_endpoint,
                             data=some_new_user_json,
                             headers=headers)

    actual = response.json()
    expected = some_new_user_response

    assert actual == expected
    assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.api
def test_create_user_already_exists(url, users_endpoint,
                                    some_new_user_json,
                                    username_conflict_response,
                                    headers):

    response = requests.post(url + users_endpoint,
                             data=some_new_user_json,
                             headers=headers)

    actual = response.json()
    expected = username_conflict_response

    assert actual == expected
    assert response.status_code == 409


@pytest.mark.integration
@pytest.mark.api
def test_create_user_email_already_exists(url, users_endpoint,
                                    new_user_same_email_json,
                                    useremail_conflict_response,
                                    headers):

    response = requests.post(url + users_endpoint,
                             data=new_user_same_email_json,
                             headers=headers)

    actual = response.json()
    expected = useremail_conflict_response

    assert actual == expected
    assert response.status_code == 409


@pytest.mark.integration
@pytest.mark.api
def test_create_corrupt_new_user(url, users_endpoint,
                                 corrupt_new_user,
                                 corrupt_new_user_conflict_response,
                                headers):

    response = requests.post(url + users_endpoint,
                             data=corrupt_new_user,
                             headers=headers)

    actual = response.json()
    expected = corrupt_new_user_conflict_response

    assert actual == expected
    assert response.status_code == 400


@pytest.mark.integration
@pytest.mark.api
def test_get_user(url, some_user_endpoint,
                  some_new_user_response,
                  headers):


    response = requests.get(url + some_user_endpoint)

    actual = response.json()
    expected = some_new_user_response

    assert actual == expected
    assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.api
def test_get_users(url, users_endpoint,
                   all_users_response):

    response = requests.get(url + users_endpoint)

    actual = response.json()
    expected = all_users_response

    assert actual == expected
    assert response.status_code == 200