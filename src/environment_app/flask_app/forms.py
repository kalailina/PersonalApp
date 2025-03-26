from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Email, Length

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

class FeedbackForm(FlaskForm):
    name = StringField('Your Name', validators=[Optional(), Length(max=100)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=100)])
    message = TextAreaField('Your Feedback', validators=[
        DataRequired(), 
        Length(min=5, max=1000, message="Feedback must be between 5 and 1000 characters")
    ])
    submit = SubmitField('Submit Feedback')