import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import movie_client
from ..forms import MovieReviewForm, SearchForm
from ..models import User, Review
from ..utils import current_time

activities = Blueprint("activities", __name__)

""" ************ View functions ************ """

# home page
@activities.route("/", methods=["GET", "POST"])
def index():
    pass

# activity page
@activities.route("/activities/<activity>", methods=["GET", "POST"])
def activity(activity):
    pass

# user page
@activities.route("/user/<username>")
def user_detail(username):
    pass
