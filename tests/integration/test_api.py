import json

import pytest
import requests

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
def endpoint(apiversion):
    return '/api/{}'.format(apiversion)

@pytest.fixture
def url(hostname, port):
    return'http://{}:{}'.format(hostname, port)


@pytest.fixture
def users_endpoint(endpoint):
    return '{}/{}'.format(endpoint, 'users')

@pytest.fixture
def endpoint_response(users_endpoint):
    return {'links':
            {'users': users_endpoint}}

@pytest.mark.integration
@pytest.mark.api
def test_api_start(url, endpoint, endpoint_response):
    response = requests.get(url+endpoint)
    assert response.status_code == 200
    actual = response.json()
    expected = endpoint_response
    assert actual == expected

@pytest.mark.integration
@pytest.mark.api
def test_users_empty(url, users_endpoint):
    response = requests.get(url+users_endpoint)
    assert response.status_code == 200
    actual = response.json()
    expected = []
    assert actual == expected

@pytest.fixture
def headers():
    return {'Content-Type': 'application/json'}

#from ..test_core import some_new_user
@pytest.fixture
def some_new_user():
    return {'name': 'bert', 'email': 'a@example.com', 'plain_password': 'abc'}

@pytest.fixture
def some_new_user_json(some_new_user):
    return json.dumps(some_new_user)

@pytest.fixture
def some_new_user_response(some_new_user, users_endpoint):
    return {'data':
            {'type': 'users',
             'id': 'bert',
             'attributes':
             {'name': 'bert',
              'email': 'a@example.com'}},
            'links': {'self': '/api/v1/users/bert'}}

@pytest.mark.integration
@pytest.mark.api
def test_create_user(url, users_endpoint,
                     some_new_user_json,
                     some_new_user_response,
                     headers):
    response = requests.post(url+users_endpoint,
                             data=some_new_user_json,
                             headers=headers)
    assert response.status_code == 200
    #actual = response.json()
    #expected = some_new_user_response
    #assert actual == expected

@pytest.mark.integration
@pytest.mark.api
def test_get_user(url, users_endpoint,
                  some_new_user_response,
                  headers):
    full_url = '{}{}/{}'.format(url, users_endpoint, 'bert')
    response = requests.get(full_url)
    assert response.status_code == 200
    actual = response.json()
    expected = some_new_user_response
    assert actual == expected
