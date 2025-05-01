from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    RadioField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired, Optional, Length, ValidationError


class InterestForm(FlaskForm):
    # Which kind of query?
    query_type = RadioField(
        "What kind of activity lookup?",
        choices=[
            ("random", "I'm bored—just give me something"),
            ("key", "I know what I want to do (by key)"),
            ("filter", "I'm picky—help me filter"),
        ],
        validators=[InputRequired()],
    )

    # If they picked the 'key' option
    activity_key = StringField(
        "Activity Key",
        validators=[Optional(), Length(min=1, max=20)],
        description="Enter the BoredAPI activity key",
    )

    # Filter options: type checkboxes
    education = BooleanField("Education")
    recreational = BooleanField("Recreational")
    social = BooleanField("Social")
    charity = BooleanField("Charity")
    cooking = BooleanField("Cooking")
    relaxation = BooleanField("Relaxation")
    busywork = BooleanField("Busywork")

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

    def validate_activity_key(self, activity_key):
        if self.query_type.data == "key":
            if not activity_key.data:
                raise ValidationError("Please provide an activity key.")

    def validate(self):
        rv = super().validate()
        if not rv:
            return False

        # If they chose filter, ensure they picked something
        if self.query_type.data == "filter":
            types_selected = any(
                getattr(self, t).data
                for t in [
                    "education",
                    "recreational",
                    "social",
                    "charity",
                    "cooking",
                    "relaxation",
                    "busywork",
                ]
            )
            if not types_selected and not self.participants.data:
                self.query_type.errors.append(
                    "Please select at least one activity type or participants."
                )
                return False

        return True
