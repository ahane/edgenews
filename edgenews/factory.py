from flask import Flask
def create_app():
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.secret_key = 'secretkey'
    from edgenews import store

    store.Registry.register('user', store.MemoryRepository('user'))
    # import flask_login
    # login_manager = flask_login.LoginManager()
    # login_manager.init_app(app)
    from edgenews.views import api
    app.register_blueprint(api)
    #from edgenews import views
    #from edgenews import models

    return app
