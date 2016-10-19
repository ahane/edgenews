# import pytest
# from edgenews import api
#
# @pytest.fixture
# def big_user():
#     return {'name': 'bert',
#             'email': 'hello@gmail.com',
#             'salt': '1234'}
#
# @pytest.fixture
# def serialized_user():
#     return {'name': 'bert',
#             'email': 'hello@gmail.com'}
#
# @pytest.mark.serialize
# def test_serialize_user(big_user, serialized_user):
#     actual = api.serialize_user(big_user)
#     expected = serialized_user
#     assert actual == expected
