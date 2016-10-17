import flask
import flask_login as loginlib
from edgenews import forms
from edgenews import interact
#from edgenews import app
api = flask.Blueprint('api', __name__, template_folder='templates')

user_manager = interact.UserManager()


login_manager = loginlib.LoginManager()
def login_user(user):
    class LoginUser(dict):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def get_id(self):
            return self['name']

        @property
        def is_active(self):
            return self['is_active']

        @property
        def is_anonymous(self):
            return self['is_anonymous']

        @property
        def is_authenticated(self):
            return self['is_authenticated']

    loginlib.login_user(LoginUser(user))


@login_manager.user_loader
def load_user(user_id):
    try:
        return user_manager.get_user(name=user_id)
    except:
        pass


@api.record_once
def on_load(state):
    login_manager.init_app(state.app)
# @api.route('/')
# def index():
#     return 'Hello World!'
#
@api.route('/signup2', methods=['GET', 'POST'])
def signup2():
    form = forms.SignupForm()
    msg = None
    if form.validate_on_submit():
        new_user = {'name': form.name.data,
                    'email': form.email.data,
                    'plain_password': form.plain_password.data}
        user, msg = user_manager.create_user(new_user)
        if msg == 'ok':
            return flask.render_template('success.html', user=user)

    return flask.render_template('signup.html', form=form, msg=msg)

@api.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user, msg = user_manager.authenticate_user(form.name.data, form.plain_password.data)
        if user is not None and msg == 'ok':
            login_user(user)
            return flask.render_template('success.html', user=user)
        else:
            return flask.render_template('login.html', msg=msg)
    return flask.render_template('login.html', form=form)



@api.route('/signup', methods=['POST'])
def signup():
    user = user_manager.create_user(flask.request.json)
    #TODO: figure out how to limit user fields!
    #login.logout_user()
    login_user(user)
    del user['salt']
    del user['hashed_password']
    #return flask.jsonify(**user)

#@login.login_required
@api.route('/whoami', methods=['GET'])
def whoami():
    current_user = loginlib.current_user
    if current_user:
        return str(current_user)
    else:
        return "couldnt find logged in user"

@api.route('/users', methods=['GET'])
def list_user():
    users = user_manager.list_users()
    return flask.render_template('users.html', users=users)
