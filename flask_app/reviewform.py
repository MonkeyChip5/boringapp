from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    RadioField,
    SelectField,
    StringField,
    SubmitField,
    IntegerField,
    TextAreaField,
)
from wtforms.validators import InputRequired, Optional, Length, ValidationError

class ActivityReviewForm(FlaskForm):
    enjoyability = IntegerField(
        "Enjoyability (1–5)",
        validators=[InputRequired()],
        render_kw={"min": 1, "max": 5}
    )
    recommendability = IntegerField(
        "Recommendability (1–5)",
        validators=[InputRequired()],
        render_kw={"min": 1, "max": 5}
    )
    stars = IntegerField(
        "Overall Rating (1–5 Stars)",
        validators=[InputRequired()],
        render_kw={"min": 1, "max": 5}
    )
    comment = TextAreaField(
        "Comment (optional)",
        validators=[Length(max=500)]
    )
    submit = SubmitField("Submit Review")