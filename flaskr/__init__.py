import os

from flask import Flask
from .models import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI='postgresql://runner:@postgres/flask_blog',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    db.init_app(app)

    from . import auth, blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")
    return app
