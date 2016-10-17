# # -*- coding: utf-8 -*-
# import pytest
# import uuid
#
# from edgenews import models
# from edgenews import app
#
#
# @pytest.fixture
# def db_name():
#     name = uuid.uuid4().hex
#     uri = 'sqlite:////tmp/{}.db'.format(name)
#     return uri
#
# @pytest.fixture
# def db(db_name):
#     app.config['SQLALCHEMY_DATABASE_URI'] = db_name
#     models.db.create_all()
#     return models.db
#
# @pytest.fixture
# def some_user():
#     return {'username': 'alec',
#             'email': 'alec@example.com',
#             'password': '123pwd'}
#
# def test_user_init(db, some_user):
#     user = models.User(**some_user)
#     db.session.add(user)
#     db.session.commit()
#
#     actual_users = models.User.query.all()
#     assert len(actual_users) == 1
