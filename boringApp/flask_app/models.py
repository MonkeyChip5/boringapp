from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True, min_length=1, max_length=40)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField()

    # Returns unique string identifying our object
    def get_id(self):
        # TODO: implement
        return str(self.username)

# change for an activity review
class Review(db.Document):
    commenter = db.ReferenceField('User', required=True)
    enjoyability = db.IntField(required=True, min_value=1, max_value=5)
    recommendability = db.IntField(required=True, min_value=1, max_value=5)
    stars = db.IntField(required=True, min_value=1, max_value=5)
    comment = db.StringField(min_length=5, max_length=500)
    date = db.StringField(required=True)
    activity_id = db.StringField(required=True, min_length=7, max_length=7)
    activity_title = db.StringField(required=True, min_length=1, max_length=200)