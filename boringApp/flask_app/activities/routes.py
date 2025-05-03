import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import movie_client
from ..forms import InterestForm
from ..models import User, Review
from ..utils import current_time

activities = Blueprint("activities", __name__)

""" ************ View functions ************ """

# home page
@activities.route("/", methods=["GET", "POST"])
def index():
    form = InterestForm()

    activity = None  # Default to no activity

    if form.validate_on_submit():
        query_type = form.query_type.data

        # Example logic—this is where you'd call the actual BoredAPI
        if query_type == "random":
            # Call BoredAPI with no parameters
            activity = {"activity": "Take a bubble bath", "type": "relaxation"}
        elif query_type == "key":
            key = form.activity_key.data
            # Call BoredAPI with ?key=...
            activity = {"activity": f"Activity for key: {key}"}
        elif query_type == "filter":
            filters = {
                "type": [t for t in [
                    "education", "recreational", "social", "charity", "cooking", "relaxation", "busywork"
                ] if getattr(form, t).data],
                "participants": form.participants.data
            }
            # Call BoredAPI with these filters
            activity = {"activity": "Filtered activity", "filters": filters}

    return render_template("index.html", form=form, activity=activity)

# activity page
@activities.route("/activities/<activity>", methods=["GET", "POST"])
def activity(activity):
    pass

# user page
@activities.route("/user/<username>")
def user_detail(username):
    pass
