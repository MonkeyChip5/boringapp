from ast import Pass
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, RadioField, SelectField, IntegerField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Optional,
    NumberRange
)

from .models import User

# Home Page: Interests Form
class InterestForm(FlaskForm):
    # Which kind of query?
    query_type = RadioField(
        "What kind of activity?",
        choices=[
            ("random", "I'm bored—just give me something"),
            ("filter", "I'm picky—help me filter (types & participants)"),
        ],
        validators=[InputRequired()],
    )
    
    # Filter options: type checkboxes
    activity_type = RadioField(
        "Types",
        choices=[
            ("education", "Education"),
            ("recreational", "Recreational"),
            ("social", "Social"),
            ("charity", "Charity"),
            ("cooking", "Cooking"),
            ("relaxation", "Relaxation"),
            ("busywork", "BusyWork"),
        ],
        validators=[Optional()],
    )

    # Filter options: number of participants
    participants = SelectField(
        "Participants",
        choices=[
            ("", "Any"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("8", "8"),
        ],
        validators=[Optional()],
    )

    submit = SubmitField("Find Activity")

    def validate(self):
        rv = super().validate()
        if not rv:
            return False

        # if they chose filter, ensure they picked something
        if self.query_type.data == "filter":
            if not self.activity_type.data and not self.participants.data:
                self.query_type.errors.append(
                    "Please select at least one activity type or participants."
                )
                return False
        return True

# Registration Page: Registration Form
class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

# Login Page: Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

# Login Page: Changing current username
class UpdateUsernameForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1,max=40)])
    submit_username = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user is not None:
                raise ValidationError("Username is taken")

# Login Page: Update user profile picture
class UpdateProfilePicForm(FlaskForm):
    picture = FileField(
        "Update Profile Picture",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "png", "jpeg"], "Images only!"),
        ],
    )
    submit_picture = SubmitField("Update")

# Review Page for a Specific Activity: Review Form
class ReviewForm(FlaskForm):
    enjoyability = IntegerField(
        "Enjoyability (1–5)",
        validators=[InputRequired(), NumberRange(min=1, max=100)]
    )
    recommendability = IntegerField(
        "Recommendability (1–5)",
        validators=[InputRequired(), NumberRange(min=1, max=100)]
    )
    stars = IntegerField(
        "Overall Rating (1–5 Stars)",
        validators=[InputRequired(), NumberRange(min=1, max=100)]
    )
    comment = TextAreaField(
        "Comment (optional)",
        validators=[Length(max=500)]
    )
    submit = SubmitField("Submit Review")
