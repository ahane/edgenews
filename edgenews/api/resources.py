import flask
from flask_restful import Resource, Api
from edgenews import interact

blueprint = flask.Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

user_manager = interact.UserManager()

class ApiResource(Resource):
    def get(self):

        return {'links':
                {'users':
                 api.url_for(UserResource)}}

class UserResource(Resource):
    def get(self):
        users, msg = user_manager.list_users()
        return users


    def post(self):
        user, msg = user_manager.create_user(flask.request.get_json())
        return user

api.add_resource(ApiResource, '/')

api.add_resource(UserResource, '/users')
