from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, ValidationError, Length
import re

class PredictionForm(FlaskForm):
    """Form for energy and emissions prediction"""
    borough = SelectField('Borough', 
        choices=[(-1, 'All Boroughs')],  # Default choice
        coerce=int, 
        validators=[Optional()]
    )
    sector = SelectField('Sector', 
        choices=[(-1, 'All Sectors')],  # Default choice
        coerce=int, 
        validators=[Optional()]
    )
    year = IntegerField('Year', validators=[
        DataRequired(),
        NumberRange(min=2022, max=2050, message="Year must be between 2022 and 2050")
    ])
    submit = SubmitField('Predict')

    def __init__(self, *args, **kwargs):
        """
        Custom initialization to populate choices dynamically.
        This allows populating choices after form instantiation.
        """
        super().__init__(*args, **kwargs)
        
        # Populate borough choices if not already set
        if len(self.borough.choices) == 1:
            from environment_app.flask_app.models import Borough
            self.borough.choices = [(-1, 'All Boroughs')] + [
                (b.borough_id, b.borough_name) for b in Borough.query.all()
            ]
        
        # Populate sector choices if not already set
        if len(self.sector.choices) == 1:
            from environment_app.flask_app.models import Sector
            self.sector.choices = [(-1, 'All Sectors')] + [
                (s.sector_id, s.sector_name) for s in Sector.query.all()
            ]

def validate_email(form, field):
    """Custom email validation without requiring email_validator package"""
    if field.data:  # Only validate if email is provided
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, field.data):
            raise ValidationError('Invalid email address.')

class FeedbackForm(FlaskForm):
    name = StringField('Your Name', validators=[Optional(), Length(max=100)])
    email = StringField('Email', validators=[Optional(), validate_email, Length(max=100)])
    message = TextAreaField('Your Feedback', validators=[
        DataRequired(message="Feedback message is required"), 
        Length(min=10, max=1000, message="Feedback must be between 10 and 1000 characters")
    ])
    submit = SubmitField('Submit Feedback')