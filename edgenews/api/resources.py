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

    def get(self):
        serialized = serialize.users(user_manager.list_users())

        return serialized

    def post(self):
        serialized = serialize.users(user_manager.create_user(flask.request.get_json()))
        return serialized


class UserResource(Resource):

    def get(self, name):
        serialized = serialize.users(user_manager.get_user(name))
        return serialized


api_object.add_resource(ApiResource, '/')

api_object.add_resource(UsersResource, '/users', endpoint='users_resource')

api_object.add_resource(UserResource, '/users/<string:name>', endpoint='user_resource')