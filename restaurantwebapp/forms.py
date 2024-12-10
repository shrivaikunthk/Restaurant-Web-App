# forms.py
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    DecimalField,
    TextAreaField,
    DateField,
    TimeField,
    IntegerField,
    FloatField,
    SelectField,
    HiddenField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    Optional,
)

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')],
    )
    phone = StringField('Phone', validators=[DataRequired(), Length(max=15)])
    location = StringField('Location', validators=[DataRequired(), Length(max=255)])
    # Removed 'role' field to prevent users from setting their own roles
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
    number_of_guests = IntegerField(
        'Number of Guests', validators=[DataRequired(), NumberRange(min=1)]
    )
    special_requests = StringField('Special Requests', validators=[Length(max=255)])
    submit = SubmitField('Reserve')

class ReviewForm(FlaskForm):
    rating = DecimalField(
        'Rating', validators=[DataRequired(), NumberRange(min=1, max=5)], places=1
    )
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Submit Review')

class SearchForm(FlaskForm):
    name = StringField('Restaurant Name', validators=[Length(max=100)])
    cuisine_type = StringField('Cuisine Type', validators=[Length(max=50)])
    min_rating = DecimalField(
        'Minimum Rating',
        validators=[Optional(), NumberRange(min=0, max=5)],
        places=1,
        default=0,
    )
    city = StringField('City', validators=[Length(max=100)])  # Added 'city' field
    submit = SubmitField('Search')

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=15)])
    location = StringField('Location', validators=[DataRequired(), Length(max=255)])
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])
    submit = SubmitField('Update Profile')

class AddToCartForm(FlaskForm):
    restaurant_id = HiddenField('Restaurant ID', validators=[DataRequired()])
    quantity = IntegerField(
        'Quantity', validators=[DataRequired(), NumberRange(min=1)], default=1
    )
    submit = SubmitField('Add to Cart')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

### **Admin Forms**

# These forms are specifically for administrative tasks and are not used by regular customers.

class CreateRestaurantAdminForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6)]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')],
    )
    phone = StringField('Phone', validators=[DataRequired(), Length(max=15)])
    restaurant_id = SelectField(
        'Restaurant',
        coerce=int,
        validators=[Optional()],
        choices=[],  # To be populated dynamically in the route
    )
    submit = SubmitField('Create Admin')

class AddRestaurantForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    address = StringField('Address', validators=[Optional(), Length(max=255)])
    city = StringField('City', validators=[Optional(), Length(max=100)])
    state = StringField('State', validators=[Optional(), Length(max=50)])
    zipcode = StringField('Zip Code', validators=[Optional(), Length(max=20)])
    website = StringField('Website', validators=[Optional(), Length(max=255)])
    cuisine_type = StringField('Cuisine Type', validators=[Optional(), Length(max=100)])
    longitude = FloatField('Longitude', validators=[Optional()])
    latitude = FloatField('Latitude', validators=[Optional()])
    number_of_tables = IntegerField(
        'Number of Tables', validators=[Optional(), NumberRange(min=1)]
    )
    max_people_per_table = IntegerField(
        'Max People per Table', validators=[Optional(), NumberRange(min=1)]
    )
    submit = SubmitField('Add Restaurant')

class EditRestaurantForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    address = StringField('Address', validators=[Optional(), Length(max=255)])
    city = StringField('City', validators=[Optional(), Length(max=100)])
    state = StringField('State', validators=[Optional(), Length(max=50)])
    zipcode = StringField('Zip Code', validators=[Optional(), Length(max=20)])
    website = StringField('Website', validators=[Optional(), Length(max=255)])
    rating = DecimalField(
        'Rating', validators=[Optional(), NumberRange(min=0, max=5)], places=1
    )
    cuisine_type = StringField('Cuisine Type', validators=[Optional(), Length(max=100)])
    longitude = FloatField('Longitude', validators=[Optional()])
    latitude = FloatField('Latitude', validators=[Optional()])
    number_of_tables = IntegerField(
        'Number of Tables', validators=[Optional(), NumberRange(min=1)]
    )
    max_people_per_table = IntegerField(
        'Max People per Table', validators=[Optional(), NumberRange(min=1)]
    )
    submit = SubmitField('Update Restaurant')

class AddMenuForm(FlaskForm):
    menu_name = StringField('Menu Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Add Menu')

class EditMenuForm(FlaskForm):
    menu_name = StringField('Menu Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Update Menu')

class AddDishForm(FlaskForm):
    dish_name = StringField('Dish Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    price = DecimalField(
        'Price',
        validators=[DataRequired(), NumberRange(min=0)],
        places=2,
    )
    submit = SubmitField('Add Dish')

class EditDishForm(FlaskForm):
    dish_name = StringField('Dish Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    price = DecimalField(
        'Price',
        validators=[DataRequired(), NumberRange(min=0)],
        places=2,
    )
    submit = SubmitField('Update Dish')

class EditReviewForm(FlaskForm):
    rating = DecimalField(
        'Rating', validators=[DataRequired(), NumberRange(min=1, max=5)], places=1
    )
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Update Review')
