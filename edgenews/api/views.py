import flask
from edgenews import interact

blueprint = flask.Blueprint('api', __name__, url_prefix='/api/v1')

user_manager = interact.UserManager()

@blueprint.route('/signup', methods=['POST'])
def signup():
    user = user_manager.create_user(flask.request.json)
    #TODO: figure out how to limit user fields!
    #login.logout_user()
    login_user(user)
    del user['salt']
    del user['hashed_password']
    #return flask.jsonify(**user)
