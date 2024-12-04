# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from forms import RegistrationForm, LoginForm, ReservationForm, ReviewForm, SearchForm
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import math

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

# Database configuration
DATABASE = 'restaurant.sqlite'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# User Loader for Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, UserID, Name, Email, Password, Phone, Location, Latitude, Longitude):
        self.id = UserID
        self.name = Name
        self.email = Email
        self.password = Password
        self.phone = Phone
        self.location = Location
        self.latitude = Latitude
        self.longitude = Longitude

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM User WHERE UserID = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['UserID'], user['Name'], user['Email'], user['Password'], user['Phone'], user['Location'], user['Latitude'], user['Longitude'])
    return None

def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate distance between two lat/lon coordinates
    R = 3959  # Radius of Earth in miles

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance

# Routes

@app.route('/')
@login_required
def home():
    user_lat = current_user.latitude
    user_lon = current_user.longitude
    conn = get_db_connection()
    restaurants = conn.execute('SELECT * FROM Restaurant').fetchall()
    restaurants_within_50_miles = []
    for restaurant in restaurants:
        rest_lat = restaurant['Latitude']
        rest_lon = restaurant['Longitude']
        distance = calculate_distance(user_lat, user_lon, rest_lat, rest_lon)
        if distance <= 50:
            restaurant = dict(restaurant)
            restaurant['Distance'] = round(distance, 2)
            restaurants_within_50_miles.append(restaurant)
    conn.close()
    return render_template('home.html', restaurants=restaurants_within_50_miles)

@app.route('/restaurants', methods=['GET', 'POST'])
@login_required
def restaurants():
    form = SearchForm()
    conn = get_db_connection()
    query = 'SELECT * FROM Restaurant WHERE 1=1'
    params = []
    if form.validate_on_submit():
        name = form.name.data
        cuisine = form.cuisine_type.data
        min_rating = form.min_rating.data
        max_distance = form.max_distance.data

        if name:
            query += ' AND Name LIKE ?'
            params.append(f'%{name}%')
        if cuisine:
            query += ' AND CuisineType LIKE ?'
            params.append(f'%{cuisine}%')
        if min_rating is not None:
            query += ' AND Rating >= ?'
            params.append(min_rating)

        restaurants = conn.execute(query, params).fetchall()
        # Calculate distance
        user_lat = current_user.latitude
        user_lon = current_user.longitude
        filtered_restaurants = []
        for restaurant in restaurants:
            rest_lat = restaurant['Latitude']
            rest_lon = restaurant['Longitude']
            distance = calculate_distance(user_lat, user_lon, rest_lat, rest_lon)
            if max_distance is not None:
                if distance <= max_distance:
                    restaurant = dict(restaurant)
                    restaurant['Distance'] = round(distance, 2)
                    filtered_restaurants.append(restaurant)
            else:
                restaurant = dict(restaurant)
                restaurant['Distance'] = round(distance, 2)
                filtered_restaurants.append(restaurant)
        restaurants = filtered_restaurants
    else:
        # If not searching, show all restaurants
        restaurants = conn.execute('SELECT * FROM Restaurant').fetchall()
        # Calculate distance
        user_lat = current_user.latitude
        user_lon = current_user.longitude
        restaurants_with_distance = []
        for restaurant in restaurants:
            rest_lat = restaurant['Latitude']
            rest_lon = restaurant['Longitude']
            distance = calculate_distance(user_lat, user_lon, rest_lat, rest_lon)
            restaurant = dict(restaurant)
            restaurant['Distance'] = round(distance, 2)
            restaurants_with_distance.append(restaurant)
        restaurants = restaurants_with_distance
    conn.close()
    return render_template('restaurants.html', restaurants=restaurants, form=form)

@app.route('/restaurant/<int:restaurant_id>')
@login_required
def restaurant(restaurant_id):
    conn = get_db_connection()
    restaurant = conn.execute('SELECT * FROM Restaurant WHERE RestaurantID = ?', (restaurant_id,)).fetchone()
    menus = conn.execute('SELECT * FROM Menu WHERE RestaurantID = ?', (restaurant_id,)).fetchall()
    conn.close()
    return render_template('restaurants.html', restaurant=restaurant, menus=menus)

@app.route('/menu/<int:menu_id>')
@login_required
def menu(menu_id):
    conn = get_db_connection()
    menu = conn.execute('SELECT * FROM Menu WHERE MenuID = ?', (menu_id,)).fetchone()
    dishes = conn.execute('SELECT * FROM Dish WHERE MenuID = ?', (menu_id,)).fetchall()
    conn.close()
    return render_template('menu.html', menu=menu, dishes=dishes)

@app.route('/dish/<int:dish_id>')
@login_required
def dish(dish_id):
    conn = get_db_connection()
    dish = conn.execute('SELECT * FROM Dish WHERE DishID = ?', (dish_id,)).fetchone()
    conn.close()
    return render_template('dish.html', dish=dish)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        phone = form.phone.data
        location = form.location.data
        latitude = form.latitude.data
        longitude = form.longitude.data

        conn = get_db_connection()
        conn.execute('INSERT INTO User (Name, Email, Password, Phone, Location, Latitude, Longitude) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (name, email, password, phone, location, latitude, longitude))
        conn.commit()
        conn.close()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM User WHERE Email = ?', (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user['Password'], form.password.data):
            user_obj = User(user['UserID'], user['Name'], user['Email'], user['Password'], user['Phone'], user['Location'], user['Latitude'], user['Longitude'])
            login_user(user_obj)
            flash('Logged in successfully!')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
@app.route('/reservations')
@login_required
def reservations():
    conn = get_db_connection()
    reservations = conn.execute('''
        SELECT r.*, res.Name AS RestaurantName
        FROM Reservation r
        JOIN Restaurant res ON r.RestaurantID = res.RestaurantID
        WHERE r.UserID = ?
        ORDER BY r.ReservationDate, r.ReservationTime
    ''', (current_user.id,)).fetchall()
    conn.close()
    return render_template('reservations.html', reservations=reservations)
@app.route('/restaurant/<int:restaurant_id>/reserve', methods=['GET', 'POST'])
@login_required
def reserve_table(restaurant_id):
    form = ReservationForm()
    if form.validate_on_submit():
        reservation_date = form.reservation_date.data.strftime('%Y-%m-%d')
        reservation_time = form.reservation_time.data.strftime('%H:%M:%S')
        number_of_guests = form.number_of_guests.data
        special_requests = form.special_requests.data

        conn = get_db_connection()
        conn.execute('INSERT INTO Reservation (UserID, RestaurantID, ReservationDate, ReservationTime, NumberOfGuests, SpecialRequests) VALUES (?, ?, ?, ?, ?, ?)',
                     (current_user.id, restaurant_id, reservation_date, reservation_time, number_of_guests, special_requests))
        conn.commit()
        conn.close()

        flash('Reservation made successfully!')
        return redirect(url_for('profile'))
    return render_template('reservations.html', form=form, restaurant_id=restaurant_id)

@app.route('/reviews')
@login_required
def reviews_overall():
    conn = get_db_connection()
    reviews = conn.execute('''
        SELECT r.*, res.Name AS RestaurantName
        FROM Review r
        JOIN Restaurant res ON r.RestaurantID = res.RestaurantID
        WHERE r.UserID = ?
        ORDER BY r.DatePosted DESC
    ''', (current_user.id,)).fetchall()
    conn.close()
    return render_template('reviews_overall.html', reviews=reviews)

@app.route('/restaurant/<int:restaurant_id>/reviews', methods=['GET', 'POST'])
@login_required
def reviews(restaurant_id):
    form = ReviewForm()
    conn = get_db_connection()
    restaurant = conn.execute('SELECT * FROM Restaurant WHERE RestaurantID = ?', (restaurant_id,)).fetchone()

    if form.validate_on_submit():
        rating = float(form.rating.data)  # Convert Decimal to float
        comment = form.comment.data
        date_posted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn.execute('INSERT INTO Review (UserID, RestaurantID, Rating, Comment, DatePosted) VALUES (?, ?, ?, ?, ?)',
                     (current_user.id, restaurant_id, rating, comment, date_posted))
        conn.commit()
        flash('Review submitted successfully!')

    reviews = conn.execute('SELECT r.*, u.Name FROM Review r JOIN User u ON r.UserID = u.UserID WHERE r.RestaurantID = ?', (restaurant_id,)).fetchall()
    conn.close()

    return render_template('review.html', reviews=reviews, restaurant=restaurant, form=form)

if __name__ == '__main__':
    app.run(debug=True)
