# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime
import os

# local
# from .client import MovieClient
from .client_new import ActivityClient

# update with your API Key
OMDB_API_KEY = '37745e75'

# do not remove these 2 lines (required for autograder to work)
if os.getenv('OMDB_API_KEY'):
    OMDB_API_KEY = os.getenv('OMDB_API_KEY')

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
# movie_client = MovieClient(OMDB_API_KEY)
activity_client = ActivityClient()

from .users.routes import users
# from .movies.routes import movies
from .activities.routes import activities
from .models import User

def custom_404(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(users)
    # app.register_blueprint(movies)
    app.register_blueprint(activities)
    app.register_error_handler(404, custom_404)

    login_manager.login_view = "users.login"

    # ✅ User loader function goes here
    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(username=user_id).first()

     # ✅ Add custom Jinja2 filter here
    def price_to_dollarsign(price):
        if price >= 0.5:
            return "$$$$"
        elif price >= 0.35:
            return "$$$"
        elif price >= 0.2:
            return "$$"
        elif price >= .1:
            return "$"
        else:
            return "Basically free!"

    app.jinja_env.filters['dollars'] = price_to_dollarsign

    return app
