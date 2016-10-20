# -*- coding: utf-8 -*-
import flask
from flask_restful import Resource, Api

from edgenews import interact
from edgenews.api import serialize

blueprint = flask.Blueprint('api', __name__, url_prefix='/api/v1')
api_object = Api(blueprint)
user_manager = interact.UserManager()


class ApiResource(Resource):

    def get(self):

        return {'links':
                {'users':
                api_object.url_for(UsersResource)}}


class UsersResource(Resource):

    @serialize.add_status_code
    def get(self):

        users = user_manager.list_users()
        response = serialize.users_to_response(users)

        return response


    @serialize.add_status_code
    def post(self):

        try:
            new_user = serialize.deserialize_user(flask.request.get_json())
            user = user_manager.create_user(new_user)
            response = serialize.users_to_response(user)

        except serialize.ValidationError as err:
            response = serialize.error_to_response(err)

        return response

class UserResource(Resource):

    @serialize.add_status_code
    def get(self, name):

        user = user_manager.get_user(name)
        response = serialize.users_to_response(user)

        return response


api_object.add_resource(ApiResource, '/')

api_object.add_resource(UsersResource, '/users', endpoint='users_resource')

api_object.add_resource(UserResource, '/users/<string:name>', endpoint='user_resource')