import base64,io
from io import BytesIO
from flask import Blueprint, render_template, session, url_for, redirect, request, flash
from flask_login import current_user, login_required

from .. import activity_client
from ..forms import InterestForm, FavoriteForm, ReviewForm
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
@activities.route("/activities", methods=["GET", "POST"])
def activity():

    activity = None

    query_type = request.args.get("query_type")
    activity_type = request.args.get("activity_type")
    participants = request.args.get("participants")
    curr_key = request.args.get("key")

    favorite_form = FavoriteForm()

    if favorite_form.validate_on_submit():
        print("SUBMITTED FAVORITE REQUEST")

        key = favorite_form.activity_key.data

        if key not in current_user.favorites:
            print("adding new favorite for activity!", key)
            current_user.favorites.append(key)
            current_user.save()
            return redirect(url_for("activities.favorites", username = current_user.username))
        else:
            print("removing favorite for activity!", key)
            current_user.favorites.remove(key)
            current_user.save()
            return redirect(url_for("activities.favorites", username = current_user.username))
    else:
        print("INVALID FORM")
        print(favorite_form.activity_key.data)


    try:
        if query_type == "random":
            activity = activity_client.get_random_activity()
        elif query_type == "filter":
            activity = activity_client.get_filtered_activity(activity_type, participants)
        elif query_type == "key":
            activity = activity_client.get_activity_by_key(curr_key)
        session['current_activity'] = activity.__dict__
        # print("current_activity: ", session.get('current_activity'))

        favorite_form.activity_key.data = activity.key
        is_favorite = current_user.is_authenticated and (activity.key in current_user.favorites)
        favorite_form.submit.label.text = "Unfavorite" if is_favorite else "Favorite"

        return render_template("activity_detail.html", activity=activity, favorite_form = favorite_form, is_favorite = None)
    except ValueError as e:
        return render_template("activity_detail.html", error_msg=str(e))

# review page
@activities.route("/review/<key>", methods=["GET", "POST"])
def reviewAnActivity(key):
    try:
        result = activity_client.get_activity_by_key(key)
    except ValueError as e:
        return render_template("review.html", error_msg=str(e))

    form = ReviewForm()

    if form.validate_on_submit():
        review = Review(
            commenter = current_user._get_current_object(),
            enjoyability = form.enjoyability.data,
            recommendability = form.recommendability.data,
            stars = form.stars.data,
            comment = form.comment.data,
            date = current_time(),
            activity_id = key,
            activity_title = result.activity,
        )
        review.save()

        return redirect(url_for('activities.user_reviews', username=review.commenter.username))
    
    reviews = Review.objects(activity_id=key)

    return render_template("review.html", form=form, reviews=reviews, title=result)
    
    # this returns the full activity, so store it's activity name using the key "activity"
    # ex: current_activity {'activity': 'Draw something interesting', 'availability': 0, 'type': 'recreational', 
    # 'participants': 1, 'price': 0, 'accessibility': 'Few to no challenges', 'duration': 'minutes', 'kid_friendly': True, 'link': '', 'key': '8033599'}
    
    # current_activity = session.get('current_activity')

# user page
@activities.route("/user/<username>")
def user_reviews(username):
    user = User.objects(username=username).first()

    if not user:
         error = "User not found"
         return render_template("reviews.html", error=error, reviews=None)
    
    reviews = Review.objects(commenter=user)

    return render_template("reviews.html", error=None, reviews=reviews)
@activities.route("/favorites", methods = ["GET", "POST"])
@login_required
def favorites():

    favorite_activities = []

    form = FavoriteForm()

    if form.validate_on_submit():

        key = form.activity_key.data

        print("valid form submission! activity key", key)

        print("removing favorite for activity!", key)
        current_user.favorites.remove(key)
        current_user.save()
        return redirect(url_for("activities.favorites"))

    else:
        print('invalid form submission! key = ', form.activity_key.data)

    for key in current_user.favorites:
        try:
            activity = activity_client.get_activity_by_key(key)

            # different forms per activity
            display_form = FavoriteForm()
            display_form.submit.label.text = "Unfavorite"
            display_form.activity_key.data = activity.key
            
            favorite_activities.append((activity, display_form))
        except ValueError as e:
            print(f"Skipping activity with key {key}: {e}")
            continue  # Skip any activity that causes a fetch error

    return render_template("favorites.html", favorites=favorite_activities)