import flask
from flask_restful import Resource, Api

from edgenews import interact
from edgenews.core.user import BaseUserSchema
from edgenews.api.serialize import as_jsonapi_and_statuscode
blueprint = flask.Blueprint('api', __name__, url_prefix='/api/v1')
api_object = Api(blueprint)
user_manager = interact.UserManager()




class ApiResource(Resource):

    def get(self):

        return {'links':
                {'users':
                api_object.url_for(UsersResource)}}

class UsersResource(Resource):

    @as_jsonapi_and_statuscode(id_field='name', type_='users', fields=['name', 'email'])
    def get(self):
        return user_manager.list_users()


    @as_jsonapi_and_statuscode(id_field='name', type_='users', fields=['name', 'email'])
    def post(self):
        return user_manager.create_user(flask.request.get_json())


class UserResource(Resource):



    @as_jsonapi_and_statuscode(id_field='name', type_='users', fields=['name', 'email'])
    def get(self, user_id):
        return user_manager.get_user(user_id)

api_object.add_resource(ApiResource, '/')

api_object.add_resource(UsersResource, '/users')

api_object.add_resource(UserResource, '/users/<string:user_id>')


def _serialize(record, schema):
    return schema().dump(record).data

def serialize_user(user):
    user['id'] = user['name']
    return _serialize(user, BaseUserSchema)
