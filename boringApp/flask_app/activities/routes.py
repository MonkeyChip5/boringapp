import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import activity_client
from ..forms import InterestForm
from ..models import User, Review
from ..utils import current_time

activities = Blueprint("activities", __name__)

""" ************ View functions ************ """

# home page
@activities.route("/", methods=["GET", "POST"])
def index():
    form = InterestForm()

    activity_type = None  # Default to no activity

    if form.validate_on_submit():
        query_type = form.query_type.data
        for t in [
                "education", "recreational", "social", "charity", "cooking", "relaxation", "busywork"
            ]:
                if getattr(form, t).data:
                    activity_type = t
                    break
        participants = form.participants.data
        
        return redirect(url_for("activities.activity", query_type=query_type, activity_type=activity_type, participants=participants))

    return render_template("index.html", form=form)

    # activity_type = None  # Default to no activity

    # if form.validate_on_submit():
    #     query_type = form.query_type.data

    #     # Example logic—this is where you'd call the actual BoredAPI
    #     if query_type == "random":
    #         # Call BoredAPI with no parameters
    #         activity = {"activity": "Take a bubble bath", "type": "relaxation"}
    #     elif query_type == "key":
    #         key = form.activity_key.data
    #         # Call BoredAPI with ?key=...
    #         activity = {"activity": f"Activity for key: {key}"}
    #     elif query_type == "filter":
    #         filters = {
    #             "activity_type": [t for t in [
    #                 "education", "recreational", "social", "charity", "cooking", "relaxation", "busywork"
    #             ] if getattr(form, t).data],
    #             "participants": form.participants.data
    #         }
    #         # Call BoredAPI with these filters
    #         activity = {"activity": "Filtered activity", "filters": filters}

    # return render_template("index.html", form=form, activity=activity)

# activity page
# @activities.route("/activities", methods=["GET", "POST"])
@activities.route("/activities", methods=["GET"])
def activity():
    form = InterestForm()

    activity = None

    query_type = request.args.get("query_type")
    activity_type = request.args.get("activity_type")
    participants = request.args.get("participants")

    try:
        if query_type == "random":
            activity = activity_client.get_random_activity()
        elif query_type == "filter":
            activity = activity_client.get_filtered_activity(activity_type, participants)

        return render_template("activity_detail.html", form=form, activity=activity)
    except ValueError as e:
        return render_template("activity_detail.html", error_msg=str(e))

# user page
@activities.route("/user/<username>")
def user_detail(username):
    pass
    # user = User.objects(username=username).first()

    # if not user:
    #     error = "User not found"
    #     return render_template("user_detail.html", error=error, image=None, username=username)
    
    # reviews = Review.objects(commenter=user)

    # return render_template("user_detail.html", error=None, username=username, reviews=reviews)
