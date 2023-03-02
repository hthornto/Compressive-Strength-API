import os
from flask import Flask, session, abort
from flask_sqlalchemy import SQLAlchemy
# from decouple import config
from flask_migrate import Migrate
import configparser

import sqlalchemy


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    config = configparser.ConfigParser()
    config.read('settings.ini')
    app.config.from_mapping(
        SECRET_KEY=config['General']["SECRET_KEY"],
        SQLALCHEMY_DATABASE_URI=config['Main Database']['DB_DIALECT'] + '://' + config['Main Database']["DB_USERNAME"] + ':' + config['Main Database']["DB_PASSWORD"] +
        '@' + config['Main Database']["DB_HOST"] + ':' +
        config['Main Database']["DB_PORT"] +
        '/' + config['Main Database']["DB_NAME"],
        SQLALCHEMY_ECHO=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        # TESTING=config("TESTING"),
        # SESSION_COOKIE_HTTPONLY=False
        SQLALCHEMY_BINDS={


        }
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models import db
    db.init_app(app)
    migrate = Migrate(app, db)
    # with app.app_context():
    #    db.create_all()
    from .api import loginapi
    app.register_blueprint(loginapi.login_api)

    # if session["loggedin"] == True:
    from .api import sets, mix_design, specimen_types, cylinders, mix_used, clients, projects  # , loginapi
    app.register_blueprint(sets.set_blueprint)
    app.register_blueprint(mix_design.bp)
    app.register_blueprint(specimen_types.speciman_types)
    app.register_blueprint(cylinders.cylinder_blueprint)
    app.register_blueprint(mix_used.mix_used_blueprint)
    app.register_blueprint(clients.bp)
    app.register_blueprint(projects.bp)
    # app.register_blueprint(loginapi.login_api)
    # else:
    #    return abort(401)
    # myapp = app.app_context()

    return app
