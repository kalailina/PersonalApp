from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Email, Length

class PredictionForm(FlaskForm):
    """Form for energy and emissions prediction"""
    borough = SelectField('Borough', validators=[Optional()], coerce=int)
    sector = SelectField('Sector', validators=[Optional()], coerce=int)
    year = IntegerField('Year', validators=[
        DataRequired(),
        NumberRange(min=2022, max=2050, message="Year must be between 2022 and 2050")
    ])

class FeedbackForm(FlaskForm):
    name = StringField('Your Name', validators=[Optional(), Length(max=100)])
    email = StringField('Email', validators=[Optional(), Length(max=100)])
    message = TextAreaField('Your Feedback', validators=[
        DataRequired(), 
        Length(min=5, max=1000, message="Feedback must be between 5 and 1000 characters")
    ])
    submit = SubmitField('Submit Feedback')