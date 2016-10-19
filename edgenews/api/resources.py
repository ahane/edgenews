import flask
from flask_restful import Resource, Api
from marshmallow_jsonapi import Schema as JsonAPISchema, fields

from edgenews import interact
from edgenews.core.user import BaseUserSchema

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
        users, msg = user_manager.list_users()
        return users

    def post(self):
        user, msg = user_manager.create_user(flask.request.get_json())
        return user

class UserResource(Resource):
    def get(self, user_id):
        user, msg = user_manager.get_user(user_id)
        return serialize_user(user)

api_object.add_resource(ApiResource, '/')

api_object.add_resource(UsersResource, '/users')

api_object.add_resource(UserResource, '/users/<string:user_id>')

#
# class UserAPISchema(JsonAPISchema, BaseUserSchema):
#     id = fields.Str(dump_only=True)
#
#     class Meta:
#         type_ = 'users'
#         self_view = api_object.url_for(UserResource)

def _serialize(record, schema):
    return schema().dump(record).data

def serialize_user(user):
    user['id'] = user['name']
    return _serialize(user, BaseUserSchema)
