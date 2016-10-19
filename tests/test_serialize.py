import pytest

from edgenews.api.serialize import as_jsonapi_and_statuscode


@pytest.fixture
def simple_record_msg():
    return {'name': 'bert', 'email': 'a@b.de', 'salt': 123}, 'ok'

@pytest.fixture
def jsonapi_record():
    return {'data':
            {'id': 'bert',
             'type': 'users',
             'attributes': {'name': 'bert', 'email': 'a@b.de'}}}

@pytest.fixture
def jsonapi_empty_result():
    return {'data': []}

@pytest.fixture
def empty_result():
    return [], 'ok'

@pytest.fixture
def no_record_error():
    return None, 'a detailed error message'

@pytest.fixture
def decorated_func():
    @as_jsonapi_and_statuscode(id_field='name', type_='users', fields=['name', 'email'])
    def some_func(param):
        return param
    return some_func

def test_simple_record(simple_record_msg, jsonapi_record, decorated_func):
    actual = decorated_func(simple_record_msg)
    expected = jsonapi_record
    assert actual == expected

def test_empty_result(empty_result, jsonapi_empty_result, decorated_func):
    actual = decorated_func(empty_result)
    expected = jsonapi_empty_result
    assert actual == expected

def test_error():
    pass