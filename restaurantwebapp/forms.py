# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, TextAreaField, DateField, TimeField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=15)])
    location = StringField('Location', validators=[DataRequired(), Length(max=255)])
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ReservationForm(FlaskForm):
    reservation_date = DateField('Reservation Date', validators=[DataRequired()])
    reservation_time = TimeField('Reservation Time', validators=[DataRequired()])
    number_of_guests = IntegerField('Number of Guests', validators=[DataRequired(), NumberRange(min=1)])
    special_requests = StringField('Special Requests', validators=[Length(max=255)])
    submit = SubmitField('Reserve')

class ReviewForm(FlaskForm):
    rating = DecimalField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit Review')

class SearchForm(FlaskForm):
    name = StringField('Restaurant Name', validators=[Length(max=100)])
    cuisine_type = StringField('Cuisine Type', validators=[Length(max=50)])
    min_rating = DecimalField('Minimum Rating', validators=[NumberRange(min=0, max=5)], places=1)
    max_distance = FloatField('Maximum Distance (miles)', validators=[NumberRange(min=0)])
    submit = SubmitField('Search')
