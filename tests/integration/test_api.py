import json

import pytest
import requests



def _request_to_jsonapi(record, type_):
    wrapped = {'data': {'type': type_, 'attributes': record}}
    return json.dumps(wrapped)

# @pytest.fixture(scope='module')
# def running_server(request):
#     from edgenews import app
#     from multiprocessing import Process
#
#     def run_server():
#         app.run(debug=True)
#
#     server = Process(target=run_server)
#     server.start()
#
#     def kill_server():
#         server.terminate()
#         server.join()
#     request.addfinalizer(kill_server)



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
    expected = {'data': [],
                'links': {'self': '/api/v1/users'}}
    assert actual == expected

@pytest.fixture
def headers():
    return {'Content-Type': 'application/json'}


@pytest.fixture
def some_new_user_json():
    user = {'name': 'bert', 'email': 'a@example.com', 'plain_password': 'abc'}
    return _request_to_jsonapi(user, 'user')

@pytest.fixture
def new_user_same_email_json():
    user = {'name': 'ernie', 'email': 'a@example.com', 'plain_password': 'abc'}
    return _request_to_jsonapi(user, 'user')


@pytest.fixture
def corrupt_new_user():
    user = {'name': 'ernie', 'emails': 'a@example.com', 'plain_password': ''}
    return _request_to_jsonapi(user, 'user')

@pytest.fixture
def some_new_user_response(users_endpoint):
    return {'links': {'self': '/api/v1/users/bert'},
            'data': {
                    'type': 'user',
                     'id': 'bert',
                     'links': {'self': '/api/v1/users/bert'},
                     'attributes': {'name': 'bert', 'email': 'a@example.com'}
                    }
           }

@pytest.fixture
def all_users_response(users_endpoint):
    return {'links': {'self': '/api/v1/users'},
            'data': [{
                    'type': 'user',
                    'id': 'bert',
                    'links': {'self': '/api/v1/users/bert'},
                    'attributes': {'name': 'bert', 'email': 'a@example.com'}
                    }]
           }

@pytest.fixture
def username_conflict_response():
    return {'errors': [ {'status': '409', 'title': 'User Already Exists', 'detail': 'username already taken'}]
           }

@pytest.fixture
def useremail_conflict_response():
    return {'errors': [ {'status': '409', 'title': 'User Already Exists', 'detail': 'email address already in use'}]
           }

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
                         'source': {'pointer': '/data/attributes/plain_password'}}
                        ]
           }

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
    actual = response.json()
    expected = some_new_user_response
    assert actual == expected

@pytest.mark.integration
@pytest.mark.api
def test_create_user_already_exists(url, users_endpoint,
                                    some_new_user_json,
                                    username_conflict_response,
                                    headers):
    response = requests.post(url+users_endpoint,
                             data=some_new_user_json,
                             headers=headers)
    assert response.status_code == 409
    actual = response.json()
    expected = username_conflict_response
    assert actual == expected

@pytest.mark.integration
@pytest.mark.api
def test_create_user_email_already_exists(url, users_endpoint,
                                    new_user_same_email_json,
                                    useremail_conflict_response,
                                    headers):
    response = requests.post(url+users_endpoint,
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
    response = requests.post(url+users_endpoint,
                             data=corrupt_new_user,
                             headers=headers)

    actual = response.json()
    expected = corrupt_new_user_conflict_response
    assert actual == expected
    assert response.status_code == 400


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

@pytest.mark.integration
@pytest.mark.api
def test_get_users(url, users_endpoint,
                   all_users_response):
    response = requests.get(url + users_endpoint)
    assert response.status_code == 200
    actual = response.json()
    expected = all_users_response
    assert actual == expected