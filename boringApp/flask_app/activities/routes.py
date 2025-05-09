import base64,io
from io import BytesIO
from flask import Blueprint, render_template, session, url_for, redirect, request, flash
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
        activity_type = form.activity_type.data
        participants = form.participants.data
        
        return redirect(url_for("activities.activity", query_type=query_type, activity_type=activity_type, participants=participants))

    return render_template("index.html", form=form)

# activity page
@activities.route("/activities", methods=["GET"])
def activity():
    form = InterestForm()

    activity = None

    query_type = request.args.get("query_type")
    activity_type = request.args.get("activity_type")
    participants = request.args.get("participants")
    loggedIn = False

    try:
        if query_type == "random":
            activity = activity_client.get_random_activity()
        elif query_type == "filter":
            activity = activity_client.get_filtered_activity(activity_type, participants)

        session['current_activity'] = activity.__dict__
        # print("current_activity: ", session.get('current_activity'))

        return render_template("activity_detail.html", form=form, activity=activity)
    except ValueError as e:
        return render_template("activity_detail.html", error_msg=str(e))


# review page
@activities.route("/reviews", methods=["GET", "POST"])
def reviewAnActivity():
    
    return render_template("review_an_activity.html")
    
    # this returns the full activity, so store it's activity name using the key "activity"
    # ex: current_activity {'activity': 'Draw something interesting', 'availability': 0, 'type': 'recreational', 
    # 'participants': 1, 'price': 0, 'accessibility': 'Few to no challenges', 'duration': 'minutes', 'kid_friendly': True, 'link': '', 'key': '8033599'}
    
    # current_activity = session.get('current_activity')

# user page
@activities.route("/user/<username>")
def user_detail(username):
    return render_template("user_detail(b).html")
    # return render_template("user_detail(b).html")
    # user = User.objects(username=username).first()

    # if not user:
    #     error = "User not found"
    #     return render_template("user_detail.html", error=error, image=None, username=username)
    
    # reviews = Review.objects(commenter=user)

    # return render_template("user_detail.html", error=None, username=username, reviews=reviews)
