import os
import sqlite3
from datetime import datetime, date, timedelta
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import (
    LoginManager, UserMixin, login_user, current_user,
    logout_user, login_required
)
from werkzeug.security import generate_password_hash, check_password_hash
from forms import (
    RegistrationForm, LoginForm, ReservationForm, ReviewForm,
    SearchForm, ProfileForm, AddToCartForm, EmptyForm,
    CreateRestaurantAdminForm, AddRestaurantForm, EditRestaurantForm,
    AddMenuForm, EditMenuForm, AddDishForm, EditDishForm, EditReviewForm
)

#basic flask app
app = Flask(__name__)
app.secret_key = 'super_secret_key' 
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'restaurant.sqlite')

#database schema, create if not there
if not os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript('''
    CREATE TABLE User (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Email TEXT UNIQUE NOT NULL,
        Password TEXT NOT NULL,
        Phone TEXT,
        Location TEXT,
        Longitude REAL,
        Latitude REAL,
        Role TEXT DEFAULT 'customer',
        ManagedRestaurantID INTEGER,
        FOREIGN KEY (ManagedRestaurantID) REFERENCES Restaurant(RestaurantID)
    );

    CREATE TABLE Restaurant (
        RestaurantID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Address TEXT,
        City TEXT,
        State TEXT,
        ZipCode TEXT,
        Website TEXT,
        Rating REAL,
        CuisineType TEXT,
        Longitude REAL,
        Latitude REAL,
        NumberOfTables INTEGER,
        MaxPeoplePerTable INTEGER
    );

    CREATE TABLE Orders (
        OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        OrderDate TEXT,
        OrderTotal REAL,
        DeliveryAddress TEXT,
        FOREIGN KEY (UserID) REFERENCES User(UserID)
    );

    CREATE TABLE DishOrder (
        DishOrderID INTEGER PRIMARY KEY AUTOINCREMENT,
        OrderID INTEGER,
        DishID INTEGER,
        Quantity INTEGER,
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
        FOREIGN KEY (DishID) REFERENCES Dish(DishID)
    );

    CREATE TABLE Review (
        ReviewID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        RestaurantID INTEGER,
        Rating REAL,
        Comment TEXT,
        DatePosted TEXT,
        FOREIGN KEY (UserID) REFERENCES User(UserID),
        FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID)
    );

    CREATE TABLE Favorites (
        FavoriteID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        RestaurantID INTEGER,
        FOREIGN KEY (UserID) REFERENCES User(UserID),
        FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID),
        UNIQUE(UserID, RestaurantID)  -- Ensures a user cannot favorite the same restaurant multiple times
    );

    CREATE TABLE Reservation (
        ReservationID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        RestaurantID INTEGER,
        ReservationDate TEXT,
        ReservationTime TEXT,
        ReservationEndTime TEXT,
        NumberOfGuests INTEGER,
        SpecialRequests TEXT,
        FOREIGN KEY (UserID) REFERENCES User(UserID),
        FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID)
    );

    CREATE TABLE Menu (
        MenuID INTEGER PRIMARY KEY AUTOINCREMENT,
        RestaurantID INTEGER,
        MenuName TEXT,
        Description TEXT,
        FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID)
    );

    CREATE TABLE Dish (
        DishID INTEGER PRIMARY KEY AUTOINCREMENT,
        MenuID INTEGER,
        DishName TEXT,
        Description TEXT,
        Price REAL,
        FOREIGN KEY (MenuID) REFERENCES Menu(MenuID)
    );
    ''')
    conn.commit()
    conn.close()
#open db
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
#login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, UserID, Name, Email, Password, Phone, Location, Longitude, Latitude, Role, ManagedRestaurantID):
        self.id = UserID
        self.name = Name
        self.email = Email
        self.password = Password
        self.phone = Phone
        self.location = Location
        self.longitude = Longitude
        self.latitude = Latitude
        self.role = Role
        self.managed_restaurant_id = ManagedRestaurantID

    @staticmethod
    def get(user_id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM User WHERE UserID = ?', (user_id,)).fetchone()
        conn.close()
        if user:
            return User(*user)
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

#jinja 2 formatting stuff
def format_datetime(value):
    """
    Formats an ISO datetime string to 'YYYY-MM-DD HH:MM:SS'.
    Removes the 'T' and microseconds.
    """
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return value  

def format_time(value):
    """
    Formats a 'HH:MM' time string to 'HH:MM:SS AM/PM'.
    Example: '10:00' -> '10:00:00 AM'
    """
    try:
        dt = datetime.strptime(value, '%H:%M')
        return dt.strftime('%I:%M:%S %p')
    except ValueError:
        return value  

app.jinja_env.filters['format_datetime'] = format_datetime
app.jinja_env.filters['format_time'] = format_time


#editing rating as restuarant is being rated
def update_restaurant_rating(restaurant_id):
    conn = get_db_connection()
    try:
        avg_rating = conn.execute('''
            SELECT AVG(Rating) as average_rating
            FROM Review
            WHERE RestaurantID = ?
        ''', (restaurant_id,)).fetchone()['average_rating']
        
        conn.execute('''
            UPDATE Restaurant
            SET Rating = ?
            WHERE RestaurantID = ?
        ''', (avg_rating, restaurant_id))
        conn.commit()
    except Exception as e:
        print(f"Error updating rating for RestaurantID {restaurant_id}: {e}")
    finally:
        conn.close()
#check user level
def is_restaurant_admin():
    return current_user.is_authenticated and current_user.role == 'restaurant_admin'
#check user level
def is_super_admin():
    return current_user.is_authenticated and current_user.role == 'super_admin'

#check to make sure restaurant isn't overfilled
def check_restaurant_capacity(restaurant_id, rdate, rstart, rend, guests):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT NumberOfTables, MaxPeoplePerTable FROM Restaurant WHERE RestaurantID = ?', (restaurant_id,))
    restaurant = cursor.fetchone()
    if not restaurant:
        conn.close()
        return False, "Restaurant not found."

    capacity = restaurant['NumberOfTables'] * restaurant['MaxPeoplePerTable']

    cursor.execute('''
        SELECT NumberOfGuests FROM Reservation
        WHERE RestaurantID = ?
          AND ReservationDate = ?
          AND ReservationTime < ?
          AND ReservationEndTime > ?
    ''', (restaurant_id, rdate, rend, rstart))
    overlapping_reservations = cursor.fetchall()

    total_guests = sum([res['NumberOfGuests'] for res in overlapping_reservations])

    conn.close()

    if total_guests + guests <= capacity:
        return True, None
    else:
        return False, "Not enough space at the requested time."

#home
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

#login autheincator
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM User WHERE Email = ?', (form.email.data,)).fetchone()
        conn.close()
        if user:
            stored_password = user['Password']
            if check_password_hash(stored_password, form.password.data):
                user_obj = User(*user)
                login_user(user_obj)
                flash('Logged in successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid password. Please try again.', 'danger')
        else:
            flash('No account found with that email.', 'danger')
    return render_template('login.html', form=form)

#logout 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

#registeration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO User (Name, Email, Password, Phone, Location, Longitude, Latitude,Role)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                form.name.data,
                form.email.data,
                hashed_password, 
                form.phone.data,
                form.location.data,
                form.longitude.data,
                form.latitude.data,
                'customer'
            ))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
        except sqlite3.IntegrityError:
            flash('Email already registered.', 'danger')
        finally:
            conn.close()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

#home page
@app.route('/home')
@login_required
def home():
    if is_super_admin():
        return redirect(url_for('super_admin_home'))
    elif is_restaurant_admin():
        return redirect(url_for('admin_home'))
    
    conn = get_db_connection()

    favorites = conn.execute('''
        SELECT Restaurant.*
        FROM Favorites
        JOIN Restaurant ON Favorites.RestaurantID = Restaurant.RestaurantID
        WHERE Favorites.UserID = ?
    ''', (current_user.id,)).fetchall()
    favorite_restaurants = favorites 
    last_order = conn.execute('''
        SELECT * FROM Orders
        WHERE UserID = ?
        ORDER BY datetime(OrderDate) DESC
        LIMIT 1
    ''', (current_user.id,)).fetchone()
    
    last_order_restaurant_name = None
    if last_order:
        dishes = conn.execute('''
            SELECT Restaurant.Name as RestaurantName
            FROM DishOrder
            JOIN Dish ON DishOrder.DishID = Dish.DishID
            JOIN Menu ON Dish.MenuID = Menu.MenuID
            JOIN Restaurant ON Menu.RestaurantID = Restaurant.RestaurantID
            WHERE DishOrder.OrderID = ?
            LIMIT 1
        ''', (last_order['OrderID'],)).fetchone()
        if dishes:
            last_order_restaurant_name = dishes['RestaurantName']

    last_review = conn.execute('''
        SELECT Review.*, Restaurant.Name as RestaurantName FROM Review
        JOIN Restaurant ON Review.RestaurantID = Restaurant.RestaurantID
        WHERE Review.UserID = ?
        ORDER BY datetime(DatePosted) DESC
        LIMIT 1
    ''', (current_user.id,)).fetchone()

    today = date.today().isoformat()
    upcoming_res = conn.execute('''
        SELECT Reservation.*, Restaurant.Name as RestaurantName
        FROM Reservation
        JOIN Restaurant ON Reservation.RestaurantID = Restaurant.RestaurantID
        WHERE Reservation.UserID = ?
          AND ReservationDate >= ?
        ORDER BY ReservationDate ASC, ReservationTime ASC
        LIMIT 1
    ''', (current_user.id, today)).fetchone()

    conn.close()

    form = EmptyForm()

    return render_template('home.html', 
                           favorite_restaurants=favorite_restaurants, 
                           last_order=last_order, 
                           last_order_restaurant_name=last_order_restaurant_name,
                           last_review=last_review, 
                           upcoming_res=upcoming_res,
                           form=form)

#show all restaurants ahh
@app.route('/restaurants', methods=['GET', 'POST'])
@login_required
def restaurants():
    form = SearchForm()
    restaurants = []

    if form.validate_on_submit():
        name = form.name.data
        cuisine = form.cuisine_type.data
        rating = form.min_rating.data
        city = form.city.data

        query = 'SELECT * FROM Restaurant WHERE 1=1'
        params = []

        if name:
            query += ' AND Name LIKE ?'
            params.append(f"%{name}%")
        if cuisine:
            query += ' AND CuisineType LIKE ?'
            params.append(f"%{cuisine}%")
        if rating:
            query += ' AND Rating >= ?'
            params.append(float(rating))
        if city:
            query += ' AND City LIKE ?'
            params.append(f"%{city}%")

        conn = get_db_connection()
        restaurants = conn.execute(query, params).fetchall()
        conn.close()

    else:
        conn = get_db_connection()
        restaurants = conn.execute('SELECT * FROM Restaurant').fetchall()
        conn.close()

    return render_template('restaurants.html', restaurants=restaurants, form=form)

#show restaurant detail based on id
@app.route('/restaurant/<int:restaurant_id>')
@login_required
def restaurant_detail(restaurant_id):
    conn = get_db_connection()
    restaurant = conn.execute('SELECT * FROM Restaurant WHERE RestaurantID = ?', (restaurant_id,)).fetchone()
    if not restaurant:
        conn.close()
        flash("Restaurant not found.", 'danger')
        return redirect(url_for('restaurants'))
    
    avg_rating = conn.execute('''
        SELECT AVG(Rating) as avg_rating FROM Review
        WHERE RestaurantID = ?
    ''', (restaurant_id,)).fetchone()['avg_rating']
    
    conn.close()

    form = EmptyForm()

    return render_template('restaurant_details.html', restaurant=restaurant, avg_rating=avg_rating, form=form)

#menu for restaurant
@app.route('/restaurant/<int:restaurant_id>/menu')
@login_required
def menu(restaurant_id):
    conn = get_db_connection()
    menus = conn.execute('SELECT * FROM Menu WHERE RestaurantID = ?', (restaurant_id,)).fetchall()
    conn.close()
    return render_template('menu.html', menus=menus, restaurant_id=restaurant_id)

@app.route('/menu/<int:menu_id>', methods=['GET', 'POST'])
@login_required
def view_menu(menu_id):
    conn = get_db_connection()
    menu = conn.execute('SELECT * FROM Menu WHERE MenuID = ?', (menu_id,)).fetchone()
    if not menu:
        conn.close()
        flash("Menu not found.", 'danger')
        return redirect(url_for('restaurants'))
    dishes = conn.execute('SELECT * FROM Dish WHERE MenuID = ?', (menu_id,)).fetchall()
    conn.close()
    

    dish_list = []
    for dish in dishes:
        dish_list.append({
            'DishID': dish['DishID'],
            'DishName': dish['DishName'],
            'Description': dish['Description'],
            'Price': dish['Price']
        })
    
    form = AddToCartForm()
    form.restaurant_id.data = menu['RestaurantID']
    restaurant_id = menu['RestaurantID']
    return render_template('dish.html', menu=menu, dishes=dish_list, form=form, restaurant_id=restaurant_id)

#reviews
@app.route('/restaurant/<int:restaurant_id>/reviews', methods=['GET', 'POST'])
@login_required
def review(restaurant_id):
    form = ReviewForm()
    if form.validate_on_submit():
        rating = form.rating.data
        comment = form.comment.data
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO Review (UserID, RestaurantID, Rating, Comment, DatePosted)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                current_user.id,
                restaurant_id,
                float(rating),
                comment,
                datetime.now().isoformat()
            ))
            conn.commit()
            flash("Review added.", 'success')
            update_restaurant_rating(restaurant_id)

        except Exception as e:
            flash("An error occurred while adding the review.", 'danger')
        finally:
            conn.close()
        return redirect(url_for('review', restaurant_id=restaurant_id))  
    
    conn = get_db_connection()
    restaurant = conn.execute('SELECT * FROM Restaurant WHERE RestaurantID = ?', (restaurant_id,)).fetchone()
    if not restaurant:
        conn.close()
        flash("Restaurant not found.", 'danger')
        return redirect(url_for('restaurants'))
    
    reviews = conn.execute('''
        SELECT Review.*, User.Name FROM Review
        JOIN User ON Review.UserID = User.UserID
        WHERE Review.RestaurantID = ?
        ORDER BY datetime(DatePosted) DESC
    ''', (restaurant_id,)).fetchall()
    
    conn.close()
    return render_template('review.html', form=form, restaurant=restaurant, reviews=reviews)

#reserving for restaurant
@app.route('/restaurant/<int:restaurant_id>/reserve', methods=['GET','POST'])
@login_required
def make_reservation(restaurant_id):
    conn = get_db_connection()
    restaurant = conn.execute('SELECT * FROM Restaurant WHERE RestaurantID = ?', (restaurant_id,)).fetchone()
    conn.close()
    if not restaurant:
        flash("Restaurant not found.", 'danger')
        return redirect(url_for('restaurants'))
    
    form = ReservationForm()
    if form.validate_on_submit():
        rdate = form.reservation_date.data.isoformat()
        rtime = form.reservation_time.data.strftime("%H:%M")
        rendtime = (datetime.combine(date.today(), form.reservation_time.data) + 
                    timedelta(hours=2)).strftime("%H:%M")  
        guests = form.number_of_guests.data
        special_req = form.special_requests.data

        try:
            start_time_obj = datetime.strptime(rtime, "%H:%M").time()
            end_time_obj = datetime.strptime(rendtime, "%H:%M").time()
            if end_time_obj <= start_time_obj:
                flash("End time must be after start time.", 'danger')
                return redirect(url_for('make_reservation', restaurant_id=restaurant_id))
        except ValueError:
            flash("Invalid time format.", 'danger')
            return redirect(url_for('make_reservation', restaurant_id=restaurant_id))

        conn = get_db_connection()
        existing = conn.execute('''
            SELECT * FROM Reservation
            WHERE RestaurantID = ?
              AND UserID = ?
              AND ReservationDate = ?
              AND ReservationTime = ?
        ''', (restaurant_id, current_user.id, rdate, rtime)).fetchone()

        if existing:
            conn.close()
            flash("You already have a reservation at that exact start time.", 'warning')
            return redirect(url_for('make_reservation', restaurant_id=restaurant_id))

        can_book, err_msg = check_restaurant_capacity(restaurant_id, rdate, rtime, rendtime, int(guests))
        if not can_book:
            conn.close()
            flash(err_msg, 'danger')
            return redirect(url_for('make_reservation', restaurant_id=restaurant_id))

        try:
            conn.execute('''
                INSERT INTO Reservation 
                (UserID, RestaurantID, ReservationDate, ReservationTime, ReservationEndTime, NumberOfGuests, SpecialRequests)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                current_user.id,
                restaurant_id,
                rdate,
                rtime,
                rendtime,
                int(guests),
                special_req
            ))
            conn.commit()
            flash("Reservation created!", 'success')
        except Exception as e:
            flash("An error occurred while creating the reservation.", 'danger')
        finally:
            conn.close()

        return redirect(url_for('home'))

    return render_template('reservation_form.html', form=form, restaurant=restaurant)


#favoriting restaurant
@app.route('/favorite/<int:restaurant_id>', methods=['POST'])
@login_required
def add_favorite(restaurant_id):
    form = EmptyForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        restaurant = conn.execute('SELECT * FROM Restaurant WHERE RestaurantID = ?', (restaurant_id,)).fetchone()
        if not restaurant:
            conn.close()
            flash("Restaurant not found.", 'danger')
            return redirect(url_for('restaurants'))
        
        existing = conn.execute('''
            SELECT * FROM Favorites
            WHERE UserID = ? AND RestaurantID = ?
        ''', (current_user.id, restaurant_id)).fetchone()
        if not existing:
            try:
                conn.execute('''
                    INSERT INTO Favorites (UserID, RestaurantID)
                    VALUES (?, ?)
                ''', (current_user.id, restaurant_id))
                conn.commit()
                flash("Restaurant added to favorites.", 'success')
            except Exception as e:
                flash("An error occurred while adding to favorites.", 'danger')
        else:
            flash("Restaurant is already in your favorites.", 'info')
        conn.close()
    else:
        flash("Invalid form submission.", 'warning')
    return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))

#delete favorite
@app.route('/remove_favorite/<int:restaurant_id>', methods=['POST'])
@login_required
def remove_favorite(restaurant_id):
    form = EmptyForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        favorite = conn.execute('''
            SELECT * FROM Favorites
            WHERE UserID = ? AND RestaurantID = ?
        ''', (current_user.id, restaurant_id)).fetchone()
        if favorite:
            try:
                conn.execute('''
                    DELETE FROM Favorites
                    WHERE FavoriteID = ?
                ''', (favorite['FavoriteID'],))
                conn.commit()
                flash("Removed from favorites.", 'success')
            except Exception as e:
                flash("An error occurred while removing from favorites.", 'danger')
        else:
            flash("Favorite not found.", 'info')
        conn.close()
    else:
        flash("Invalid form submission.", 'warning')
    return redirect(url_for('home'))

#cart 0 adding to orders
@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    if request.method == 'POST':
        delivery_address = request.form.get('delivery_address')
        if not delivery_address:
            flash('Please provide a delivery address.', 'warning')
            return redirect(url_for('cart'))
        
        cart = session.get('cart', [])
        if not cart:
            flash('Your cart is empty.', 'info')
            return redirect(url_for('home'))
        
        conn = get_db_connection()
        try:
            order_date = datetime.now().isoformat()
            conn.execute('''
                INSERT INTO Orders (UserID, OrderDate, OrderTotal, DeliveryAddress)
                VALUES (?, ?, ?, ?)
            ''', (
                current_user.id,
                order_date,
                0.0,  
                delivery_address
            ))
            order_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        
            total = 0.0
            for item in cart:
                dish = conn.execute('SELECT * FROM Dish WHERE DishID = ?', (item['dish_id'],)).fetchone()
                if dish:
                    conn.execute('''
                        INSERT INTO DishOrder (OrderID, DishID, Quantity)
                        VALUES (?, ?, ?)
                    ''', (
                        order_id,
                        dish['DishID'],
                        item['quantity']
                    ))
                    total += dish['Price'] * item['quantity']
        
            conn.execute('UPDATE Orders SET OrderTotal = ? WHERE OrderID = ?', (total, order_id))
            conn.commit()
            session['cart'] = []  
            flash("Order placed successfully!", 'success')
        except Exception as e:
            conn.rollback()
            flash("An error occurred while placing the order.", 'danger')
        finally:
            conn.close()
        
        return redirect(url_for('home'))
    
    cart_items = session.get('cart', [])
    detailed_cart = []
    total = 0.0
    for item in cart_items:
        dish = get_dish_details(item['dish_id'])
        if dish:
            item_total = dish['Price'] * item['quantity']
            total += item_total
            detailed_cart.append({
                'dish_id': dish['DishID'],
                'dish_name': dish['DishName'],
                'price': dish['Price'],
                'quantity': item['quantity'],
                'item_total': item_total
            })
    
    form = EmptyForm()  
    
    return render_template('cart.html', cart_items=detailed_cart, total=total, form=form)

#dish details specifications
def get_dish_details(dish_id):
    conn = get_db_connection()
    dish = conn.execute('SELECT * FROM Dish WHERE DishID = ?', (dish_id,)).fetchone()
    conn.close()
    return dish

#add something cart
@app.route('/add_to_cart/<int:dish_id>', methods=['POST'])
@login_required
def add_to_cart_route(dish_id):
    form = AddToCartForm()
    if form.validate_on_submit():
        quantity = form.quantity.data
        restaurant_id = form.restaurant_id.data if form.restaurant_id.data else None
    else:
        flash("Invalid form submission.", 'warning')
        return redirect(url_for('restaurants'))

    cart = session.get('cart', [])
    
    if cart:
        existing_restaurant_id = cart[0].get('restaurant_id')
        if existing_restaurant_id != restaurant_id:
            flash("You can only add dishes from one restaurant at a time. Please clear your cart before adding dishes from a different restaurant.", 'warning')
            return redirect(url_for('cart'))
    for item in cart:
        if item['dish_id'] == dish_id:
            item['quantity'] += quantity
            break
    else:
        cart.append({'dish_id': dish_id, 'quantity': quantity, 'restaurant_id': restaurant_id})
    
    session['cart'] = cart
    flash('Dish added to cart.', 'success')
    return redirect(url_for('menu', restaurant_id=restaurant_id))

#remove from cart
@app.route('/remove_from_cart/<int:dish_id>', methods=['POST'])
@login_required
def remove_from_cart(dish_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['dish_id'] != dish_id]
    session['cart'] = cart
    flash('Dish removed from cart.', 'info')
    return redirect(url_for('cart'))


#user-profile
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        try:
            conn.execute('''
                UPDATE User
                SET Name = ?, Email = ?, Phone = ?, Location = ?, Latitude = ?, Longitude = ?
                WHERE UserID = ?
            ''', (
                form.name.data,
                form.email.data,
                form.phone.data,
                form.location.data,
                form.latitude.data,
                form.longitude.data,
                current_user.id
            ))
            conn.commit()
            flash('Profile updated successfully.', 'success')
        except sqlite3.IntegrityError:
            flash('Email already in use.', 'danger')
        except Exception as e:
            flash('An error occurred while updating the profile.', 'danger')
        finally:
            conn.close()
        return redirect(url_for('profile'))
    else:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM User WHERE UserID = ?', (current_user.id,)).fetchone()
        conn.close()
        if user:
            form.name.data = user['Name']
            form.email.data = user['Email']
            form.phone.data = user['Phone']
            form.location.data = user['Location']
            form.latitude.data = user['Latitude']
            form.longitude.data = user['Longitude']

    return render_template('profile.html', form=form)

#admin-profile
@app.route('/admin_profile')
@login_required
def admin_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        try:
            conn.execute('''
                UPDATE User
                SET Name = ?, Email = ?, Phone = ?, Location = ?, Latitude = ?, Longitude = ?
                WHERE UserID = ?
            ''', (
                form.name.data,
                form.email.data,
                form.phone.data,
                form.location.data,
                form.latitude.data,
                form.longitude.data,
                current_user.id
            ))
            conn.commit()
            flash('Profile updated successfully.', 'success')
        except sqlite3.IntegrityError:
            flash('Email already in use.', 'danger')
        except Exception as e:
            flash('An error occurred while updating the profile.', 'danger')
        finally:
            conn.close()
        return redirect(url_for('profile'))
    else:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM User WHERE UserID = ?', (current_user.id,)).fetchone()
        conn.close()
        if user:
            form.name.data = user['Name']
            form.email.data = user['Email']
            form.phone.data = user['Phone']
            form.location.data = user['Location']
            form.latitude.data = user['Latitude']
            form.longitude.data = user['Longitude']

    return render_template('profile_admin.html', form=form)

#admin-home route
@app.route('/admin_home')
@login_required
def admin_home():
    if not (is_restaurant_admin() or is_super_admin()):
        flash("Access denied.", 'danger')
        return redirect(url_for('home'))
    
    if is_super_admin():
        return redirect(url_for('super_admin_home'))
    
    conn = get_db_connection()
    restaurant_id = current_user.managed_restaurant_id
    restaurant = conn.execute('SELECT * FROM Restaurant WHERE RestaurantID = ?', (restaurant_id,)).fetchone()
    conn.close()
    return render_template('admin_home.html', restaurant=restaurant)

#admin manage reservations
@app.route('/admin/manage_reservations', methods=['GET', 'POST'])
@login_required
def admin_manage_reservation():
    if not (is_super_admin() or is_restaurant_admin()):
        flash("Access denied.", 'danger')
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    

    restaurant_id = request.args.get('restaurant_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = 10  
    
    if is_restaurant_admin():
        current_restaurant_id = current_user.managed_restaurant_id
        query = '''
            SELECT Reservation.*, User.Name as CustomerName
            FROM Reservation
            JOIN User ON Reservation.UserID = User.UserID
            WHERE Reservation.RestaurantID = ?
            ORDER BY ReservationDate DESC
            LIMIT ? OFFSET ?
        '''
        reservations = conn.execute(query, (current_restaurant_id, per_page, (page - 1) * per_page)).fetchall()
        
        total = conn.execute('SELECT COUNT(*) FROM Reservation WHERE RestaurantID = ?', (current_restaurant_id,)).fetchone()[0]
        total_pages = (total + per_page - 1) // per_page
    elif is_super_admin():
        if restaurant_id:
            query = '''
                SELECT Reservation.*, User.Name as CustomerName, Restaurant.Name as RestaurantName
                FROM Reservation
                JOIN User ON Reservation.UserID = User.UserID
                JOIN Restaurant ON Reservation.RestaurantID = Restaurant.RestaurantID
                WHERE Reservation.RestaurantID = ?
                ORDER BY ReservationDate DESC
                LIMIT ? OFFSET ?
            '''
            reservations = conn.execute(query, (restaurant_id, per_page, (page - 1) * per_page)).fetchall()
            
            
            total = conn.execute('SELECT COUNT(*) FROM Reservation WHERE RestaurantID = ?', (restaurant_id,)).fetchone()[0]
            total_pages = (total + per_page - 1) // per_page
        else:
            query = '''
                SELECT Reservation.*, User.Name as CustomerName, Restaurant.Name as RestaurantName
                FROM Reservation
                JOIN User ON Reservation.UserID = User.UserID
                JOIN Restaurant ON Reservation.RestaurantID = Restaurant.RestaurantID
                ORDER BY ReservationDate DESC
                LIMIT ? OFFSET ?
            '''
            reservations = conn.execute(query, (per_page, (page - 1) * per_page)).fetchall()
            
            
            total = conn.execute('SELECT COUNT(*) FROM Reservation').fetchone()[0]
            total_pages = (total + per_page - 1) // per_page

    
    if is_super_admin():
        restaurants = conn.execute('SELECT * FROM Restaurant').fetchall()
    else:
        restaurants = []
    
    conn.close()
    
    class Pagination:
        def __init__(self, page, total_pages):
            self.page = page
            self.total_pages = total_pages
            self.has_prev = page > 1
            self.has_next = page < total_pages
            self.prev_num = page - 1
            self.next_num = page + 1
            self.pages = total_pages

        def iter_pages(self, left_edge=2, right_edge=2, left_current=2, right_current=2):
            last = 0
            for num in range(1, self.total_pages + 1):
                if num <= left_edge or \
                   (num > self.page - left_current -1 and num < self.page + right_current) or \
                   num > self.total_pages - right_edge:
                    if last + 1 != num:
                        yield None
                    yield num
                    last = num

    pagination = Pagination(page, total_pages)
    form = EmptyForm()
    return render_template('admin_manage_reservations.html', 
                           reservations=reservations, 
                           restaurants=restaurants,
                           pagination=pagination,
                           form = form)


#edit reservation as restaurant admin
@app.route('/admin/edit_reservation/<int:reservation_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_reservation(reservation_id):
    if not (is_restaurant_admin() or is_super_admin()):
        flash("Access denied.", 'danger')
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    reservation = conn.execute('SELECT * FROM Reservation WHERE ReservationID = ?', (reservation_id,)).fetchone()
    if not reservation:
        conn.close()
        flash("Reservation not found.", 'danger')
        return redirect(url_for('admin_manage_reservation'))
    
    
    if is_restaurant_admin() and reservation['RestaurantID'] != current_user.managed_restaurant_id:
        conn.close()
        flash("Access denied.", 'danger')
        return redirect(url_for('admin_manage_reservation'))
    
    form = ReservationForm()
    if request.method == 'POST' and form.validate_on_submit():
        rdate = form.reservation_date.data.isoformat()
        rtime = form.reservation_time.data.strftime("%H:%M")
        rendtime = (datetime.combine(date.today(), form.reservation_time.data) + 
                    timedelta(hours=2)).strftime("%H:%M")  
        guests = form.number_of_guests.data
        special_req = form.special_requests.data

        
        try:
            start_time_obj = datetime.strptime(rtime, "%H:%M").time()
            end_time_obj = datetime.strptime(rendtime, "%H:%M").time()
            if end_time_obj <= start_time_obj:
                flash("End time must be after start time.", 'danger')
                return redirect(url_for('admin_edit_reservation', reservation_id=reservation_id))
        except ValueError:
            flash("Invalid time format.", 'danger')
            return redirect(url_for('admin_edit_reservation', reservation_id=reservation_id))

        can_book, err_msg = check_restaurant_capacity(reservation['RestaurantID'], rdate, rtime, rendtime, int(guests))
        if not can_book and (rdate != reservation['ReservationDate'] or rtime != reservation['ReservationTime']):
            conn.close()
            flash(err_msg, 'danger')
            return redirect(url_for('admin_edit_reservation', reservation_id=reservation_id))
        
        try:
            conn.execute('''
                UPDATE Reservation
                SET ReservationDate = ?, ReservationTime = ?, ReservationEndTime = ?, 
                    NumberOfGuests = ?, SpecialRequests = ?
                WHERE ReservationID = ?
            ''', (
                rdate,
                rtime,
                rendtime,
                int(guests),
                special_req,
                reservation_id
            ))
            conn.commit()
            flash("Reservation updated successfully.", 'success')
        except Exception as e:
            flash("An error occurred while updating the reservation.", 'danger')
        finally:
            conn.close()
        return redirect(url_for('admin_manage_reservation'))
    
    
    form.reservation_date.data = datetime.fromisoformat(reservation['ReservationDate']).date()
    form.reservation_time.data = datetime.strptime(reservation['ReservationTime'], "%H:%M").time()
    form.number_of_guests.data = reservation['NumberOfGuests']
    form.special_requests.data = reservation['SpecialRequests']
    conn.close()
    return render_template('admin_edit_reservation_form.html', form=form, reservation=reservation)


#delete reservation as a restaurant admin 
@app.route('/admin/delete_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def admin_delete_reservation(reservation_id):
    if not (is_restaurant_admin() or is_super_admin()):
        flash("Access denied.", 'danger')
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    reservation = conn.execute('SELECT * FROM Reservation WHERE ReservationID = ?', (reservation_id,)).fetchone()
    if not reservation:
        conn.close()
        flash("Reservation not found.", 'danger')
        return redirect(url_for('admin_manage_reservation'))
    
    if is_restaurant_admin() and reservation['RestaurantID'] != current_user.managed_restaurant_id:
        conn.close()
        flash("Access denied.", 'danger')
        return redirect(url_for('admin_manage_reservation'))
    
    try:
        conn.execute('DELETE FROM Reservation WHERE ReservationID = ?', (reservation_id,))
        conn.commit()
        flash("Reservation deleted successfully.", 'success')
    except Exception as e:
        flash("An error occurred while deleting the reservation.", 'danger')
    finally:
        conn.close()
    return redirect(url_for('admin_manage_reservation'))

#edit restaurant as restaurant admin
@app.route('/admin/edit_restaurant', methods=['GET', 'POST'])
@login_required
def admin_edit_restaurant():
    if not (is_restaurant_admin() or is_super_admin()):
        flash("Access denied.", 'danger')
        return redirect(url_for('home'))
    
    form = EditRestaurantForm()
    conn = get_db_connection()
    
    if is_restaurant_admin():
        restaurant_id = current_user.managed_restaurant_id
        restaurant = conn.execute('SELECT * FROM Restaurant WHERE RestaurantID = ?', (restaurant_id,)).fetchone()
    elif is_super_admin():
        restaurant_id = request.args.get('restaurant_id', type=int)
        if not restaurant_id:
            flash("Restaurant ID is required.", 'warning')
            return redirect(url_for('super_admin_home'))
        restaurant = conn.execute('SELECT * FROM Restaurant WHERE RestaurantID = ?', (restaurant_id,)).fetchone()
    
    if not restaurant:
        conn.close()
        flash("Restaurant not found.", 'danger')
        return redirect(url_for('admin_home'))
    
    if request.method == 'POST' and form.validate_on_submit():
        try:
            conn.execute('''
                UPDATE Restaurant
                SET Name = ?, Address = ?, City = ?, State = ?, ZipCode = ?, 
                    Website = ?, Rating = ?, CuisineType = ?, Longitude = ?, 
                    Latitude = ?, NumberOfTables = ?, MaxPeoplePerTable = ?
                WHERE RestaurantID = ?
            ''', (
                form.name.data,
                form.address.data,
                form.city.data,
                form.state.data,
                form.zipcode.data,
                form.website.data,
                float(form.rating.data) if form.rating.data else None,
                form.cuisine_type.data,
                float(form.longitude.data) if form.longitude.data else None,
                float(form.latitude.data) if form.latitude.data else None,
                int(form.number_of_tables.data) if form.number_of_tables.data else None,
                int(form.max_people_per_table.data) if form.max_people_per_table.data else None,
                restaurant_id
            ))
            conn.commit()
            flash("Restaurant details updated successfully.", 'success')
        except Exception as e:
            flash("An error occurred while updating restaurant details.", 'danger')
        finally:
            conn.close()
        return redirect(url_for('admin_edit_restaurant', restaurant_id=restaurant_id))
    
    form.name.data = restaurant['Name']
    form.address.data = restaurant['Address']
    form.city.data = restaurant['City']
    form.state.data = restaurant['State']
    form.zipcode.data = restaurant['ZipCode']
    form.website.data = restaurant['Website']
    form.rating.data = restaurant['Rating']
    form.cuisine_type.data = restaurant['CuisineType']
    form.longitude.data = restaurant['Longitude']
    form.latitude.data = restaurant['Latitude']
    form.number_of_tables.data = restaurant['NumberOfTables']
    form.max_people_per_table.data = restaurant['MaxPeoplePerTable']
    
    conn.close()
    return render_template('admin_edit_restaurant.html', form=form, restaurant=restaurant)

#change menu as restaurant admin
@app.route('/admin/manage_menu', methods=['GET', 'POST'])
@login_required
def admin_manage_menu():
    if not (is_restaurant_admin() or is_super_admin()):
        flash("Access denied.", 'danger')
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    if is_restaurant_admin():
        restaurant_id = current_user.managed_restaurant_id
        menus = conn.execute('SELECT * FROM Menu WHERE RestaurantID = ?', (restaurant_id,)).fetchall()
    elif is_super_admin():
        restaurant_id = request.args.get('restaurant_id', type=int)
        if not restaurant_id:
            flash("Restaurant ID is required.", 'warning')
            return redirect(url_for('super_admin_home'))
        menus = conn.execute('SELECT * FROM Menu WHERE RestaurantID = ?', (restaurant_id,)).fetchall()
    
    menu_dishes = {}
    for menu in menus:
        dishes = conn.execute('SELECT * FROM Dish WHERE MenuID = ?', (menu['MenuID'],)).fetchall()
        menu_dishes[menu['MenuID']] = dishes
    
    if is_super_admin():
        restaurant = conn.execute('SELECT * FROM Restaurant WHERE RestaurantID = ?', (restaurant_id,)).fetchone()
    else:
        restaurant = conn.execute('SELECT * FROM Restaurant WHERE RestaurantID = ?', (restaurant_id,)).fetchone()
    
    conn.close()
    return render_template('admin_manage_menu.html', menus=menus, menu_dishes=menu_dishes, restaurant=restaurant)

#add menu as a restaurant admin
@app.route('/admin/add_menu', methods=['GET', 'POST'])
@login_required
def admin_add_menu():
    if not (is_restaurant_admin() or is_super_admin()):
        flash("Access denied.", 'danger')
        return redirect(url_for('home'))
    
    form = AddMenuForm()
    conn = get_db_connection()
    
    if is_restaurant_admin():
        restaurant_id = current_user.managed_restaurant_id
    elif is_super_admin():
        restaurant_id = request.args.get('restaurant_id', type=int)
        if not restaurant_id:
            flash("Restaurant ID is required.", 'warning')
            return redirect(url_for('super_admin_home'))
    
    if request.method == 'POST' and form.validate_on_submit():
        try:
            conn.execute('''
                INSERT INTO Menu (RestaurantID, MenuName, Description)
                VALUES (?, ?, ?)
            ''', (
                restaurant_id,
                form.menu_name.data,
                form.description.data
            ))
            conn.commit()
            flash("Menu added successfully.", 'success')
        except Exception as e:
            flash("An error occurred while adding the menu.", 'danger')
        finally:
            conn.close()
        return redirect(url_for('admin_manage_menu', restaurant_id=restaurant_id))
    
    conn.close()
    return render_template('admin_add_menu.html', form=form, restaurant_id=restaurant_id)

#edit menu 
@app.route('/admin/edit_menu/<int:menu_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_menu(menu_id):
    if not (is_restaurant_admin() or is_super_admin()):
        flash("Access denied.", 'danger')
        return redirect(url_for('home'))
    
    form = EditMenuForm()
    conn = get_db_connection()
    menu = conn.execute('SELECT * FROM Menu WHERE MenuID = ?', (menu_id,)).fetchone()
    if not menu:
        conn.close()
        flash("Menu not found.", 'danger')
        return redirect(url_for('admin_manage_menu'))
    
    if is_restaurant_admin() and menu['RestaurantID'] != current_user.managed_restaurant_id:
        conn.close()
        flash("Access denied.", 'danger')
        return redirect(url_for('admin_manage_menu'))
    
    if request.method == 'POST' and form.validate_on_submit():
        try:
            conn.execute('''
                UPDATE Menu
                SET MenuName = ?, Description = ?
                WHERE MenuID = ?
            ''', (
                form.menu_name.data,
                form.description.data,
                menu_id
            ))
            conn.commit()
            flash("Menu updated successfully.", 'success')
        except Exception as e:
            flash("An error occurred while updating the menu.", 'danger')
        finally:
            conn.close()
        return redirect(url_for('admin_manage_menu', restaurant_id=menu['RestaurantID']))
    
    form.menu_name.data = menu['MenuName']
    form.description.data = menu['Description']
    
    conn.close()
    return render_template('admin_edit_menu.html', form=form, menu=menu)

#delete menu as restaurant admin
@app.route('/admin/delete_menu/<int:menu_id>', methods=['POST'])
@login_required
def admin_delete_menu(menu_id):
    if not (is_restaurant_admin() or is_super_admin()):
        flash("Access denied.", 'danger')
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    menu = conn.execute('SELECT * FROM Menu WHERE MenuID = ?', (menu_id,)).fetchone()
    if not menu:
        conn.close()
        flash("Menu not found.", 'danger')
        return redirect(url_for('admin_manage_menu'))
    
    if is_restaurant_admin() and menu['RestaurantID'] != current_user.managed_restaurant_id:
        conn.close()
        flash("Access denied.", 'danger')
        return redirect(url_for('admin_manage_menu'))
    
    try:
        conn.execute('DELETE FROM Dish WHERE MenuID = ?', (menu_id,))
        conn.execute('DELETE FROM Menu WHERE MenuID = ?', (menu_id,))
        conn.commit()
        flash("Menu and its dishes deleted successfully.", 'success')
    except Exception as e:
        flash("An error occurred while deleting the menu.", 'danger')
    finally:
        conn.close()
    return redirect(url_for('admin_manage_menu', restaurant_id=menu['RestaurantID']))

#add dish to menu as a restaurant admin
@app.route('/admin/add_dish/<int:menu_id>', methods=['GET', 'POST'])
@login_required
def admin_add_dish(menu_id):
    if not (is_restaurant_admin() or is_super_admin()):
        flash("Access denied.", 'danger')
        return redirect(url_for('home'))
    
    form = AddDishForm()
    conn = get_db_connection()
    menu = conn.execute('SELECT * FROM Menu WHERE MenuID = ?', (menu_id,)).fetchone()
    if not menu:
        conn.close()
        flash("Menu not found.", 'danger')
        return redirect(url_for('admin_manage_menu'))
    
    if is_restaurant_admin() and menu['RestaurantID'] != current_user.managed_restaurant_id:
        conn.close()
        flash("Access denied.", 'danger')
        return redirect(url_for('admin_manage_menu'))
    
    if request.method == 'POST' and form.validate_on_submit():
        try:
            conn.execute('''
                INSERT INTO Dish (MenuID, DishName, Description, Price)
                VALUES (?, ?, ?, ?)
            ''', (
                menu_id,
                form.dish_name.data,
                form.description.data,
                float(form.price.data)
            ))
            conn.commit()
            flash("Dish added successfully.", 'success')
        except Exception as e:
            flash("An error occurred while adding the dish.", 'danger')
        finally:
            conn.close()
        return redirect(url_for('admin_manage_menu', restaurant_id=menu['RestaurantID']))
    
    conn.close()
    return render_template('admin_add_dish.html', form=form, menu=menu)

#edit dish as restaurant admin
@app.route('/admin/edit_dish/<int:dish_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_dish(dish_id):
    if not (is_restaurant_admin() or is_super_admin()):
        flash("Access denied.", 'danger')
        return redirect(url_for('home'))
    
    form = EditDishForm()
    conn = get_db_connection()
    dish = conn.execute('SELECT * FROM Dish WHERE DishID = ?', (dish_id,)).fetchone()
    if not dish:
        conn.close()
        flash("Dish not found.", 'danger')
        return redirect(url_for('admin_manage_menu'))
    
    menu = conn.execute('SELECT * FROM Menu WHERE MenuID = ?', (dish['MenuID'],)).fetchone()
    
    if is_restaurant_admin() and menu['RestaurantID'] != current_user.managed_restaurant_id:
        conn.close()
        flash("Access denied.", 'danger')
        return redirect(url_for('admin_manage_menu'))
    
    if request.method == 'POST' and form.validate_on_submit():
        try:
            conn.execute('''
                UPDATE Dish
                SET DishName = ?, Description = ?, Price = ?
                WHERE DishID = ?
            ''', (
                form.dish_name.data,
                form.description.data,
                float(form.price.data),
                dish_id
            ))
            conn.commit()
            flash("Dish updated successfully.", 'success')
        except Exception as e:
            flash("An error occurred while updating the dish.", 'danger')
        finally:
            conn.close()
        return redirect(url_for('admin_manage_menu', restaurant_id=menu['RestaurantID']))
    
    form.dish_name.data = dish['DishName']
    form.description.data = dish['Description']
    form.price.data = dish['Price']
    
    conn.close()
    return render_template('admin_edit_dish.html', form=form, dish=dish)

#delete dish as restaurant admin
@app.route('/admin/delete_dish/<int:dish_id>', methods=['POST'])
@login_required
def admin_delete_dish(dish_id):
    if not (is_restaurant_admin() or is_super_admin()):
        flash("Access denied.", 'danger')
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    dish = conn.execute('SELECT * FROM Dish WHERE DishID = ?', (dish_id,)).fetchone()
    if not dish:
        conn.close()
        flash("Dish not found.", 'danger')
        return redirect(url_for('admin_manage_menu'))
    
    menu = conn.execute('SELECT * FROM Menu WHERE MenuID = ?', (dish['MenuID'],)).fetchone()
    
    if is_restaurant_admin() and menu['RestaurantID'] != current_user.managed_restaurant_id:
        conn.close()
        flash("Access denied.", 'danger')
        return redirect(url_for('admin_manage_menu'))
    
    try:
        conn.execute('DELETE FROM Dish WHERE DishID = ?', (dish_id,))
        conn.commit()
        flash("Dish deleted successfully.", 'success')
    except Exception as e:
        flash("An error occurred while deleting the dish.", 'danger')
    finally:
        conn.close()
    return redirect(url_for('admin_manage_menu', restaurant_id=menu['RestaurantID']))

#create restaurant admin as super-admin
@app.route('/admin/create_restaurant_admin', methods=['GET','POST'])
@login_required
def create_restaurant_admin():
    if not is_super_admin():
        flash("Access denied. Only super admins can create restaurant admins.", 'danger')
        return redirect(url_for('home'))
    
    form = CreateRestaurantAdminForm()
    conn = get_db_connection()
    restaurants = conn.execute('SELECT * FROM Restaurant').fetchall()
    form.restaurant_id.choices = [(-1, "None")] + [(r['RestaurantID'], r['Name']) for r in restaurants]
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        phone = form.phone.data
        restaurant_id = form.restaurant_id.data if form.restaurant_id.data != -1 else None
        hashed = generate_password_hash(password, method='sha256')
        try:
            conn.execute('''
                INSERT INTO User (Name, Email, Password, Phone, Role, ManagedRestaurantID)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                name,
                email,
                hashed,
                phone,
                'restaurant_admin',
                restaurant_id
            ))
            conn.commit()
            flash("Restaurant admin created successfully.", 'success')
        except sqlite3.IntegrityError:
            flash("Email already registered.", 'danger')
        except Exception as e:
            flash("An error occurred while creating the restaurant admin.", 'danger')
        finally:
            conn.close()
        return redirect(url_for('super_admin_home'))
    
    conn.close()
    return render_template('create_restaurant_admin.html', form=form)

#manage reviews as super admin
@app.route('/admin/manage_reviews', methods=['GET', 'POST'])
@login_required
def admin_manage_reviews():
    if not is_super_admin():
        flash("Access denied. Only super admins can manage reviews.", 'danger')
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    reviews = conn.execute('''
        SELECT Review.*, User.Name as ReviewerName, Restaurant.Name as RestaurantName
        FROM Review
        JOIN User ON Review.UserID = User.UserID
        JOIN Restaurant ON Review.RestaurantID = Restaurant.RestaurantID
        ORDER BY datetime(DatePosted) DESC
    ''').fetchall()
    conn.close()
    
    form = EmptyForm()
    return render_template('admin_manage_reviews.html', reviews=reviews, form=form)

#delete review as super admin
@app.route('/admin/delete_review/<int:review_id>', methods=['POST'])
@login_required
def admin_delete_review(review_id):
    if not is_super_admin():
        flash("Access denied. Only super admins can delete reviews.", 'danger')
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    review = conn.execute('SELECT * FROM Review WHERE ReviewID = ?', (review_id,)).fetchone()
    if not review:
        conn.close()
        flash("Review not found.", 'danger')
        return redirect(url_for('admin_manage_reviews'))
    
    try:
        conn.execute('DELETE FROM Review WHERE ReviewID = ?', (review_id,))
        conn.commit()
        flash("Review deleted successfully.", 'success')
        update_restaurant_rating(review['RestaurantID'])
    except Exception as e:
        flash("An error occurred while deleting the review.", 'danger')
    finally:
        conn.close()
    return redirect(url_for('admin_manage_reviews'))

#add restaurant as super admin
@app.route('/admin/add_restaurant', methods=['GET', 'POST'])
@login_required
def add_restaurant():
    if not is_super_admin():
        flash("Access denied. Only super admins can add restaurants.", 'danger')
        return redirect(url_for('home'))
    
    form = AddRestaurantForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO Restaurant 
                (Name, Address, City, State, ZipCode, Website, CuisineType, Longitude, Latitude, NumberOfTables, MaxPeoplePerTable)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                form.name.data,
                form.address.data,
                form.city.data,
                form.state.data,
                form.zipcode.data,
                form.website.data,
                form.cuisine_type.data,
                float(form.longitude.data) if form.longitude.data else None,
                float(form.latitude.data) if form.latitude.data else None,
                int(form.number_of_tables.data) if form.number_of_tables.data else None,
                int(form.max_people_per_table.data) if form.max_people_per_table.data else None
            ))
            conn.commit()
            flash("Restaurant added successfully.", 'success')
        except Exception as e:
            flash("An error occurred while adding the restaurant.", 'danger')
        finally:
            conn.close()
        return redirect(url_for('super_admin_home'))
    
    return render_template('add_restaurant.html', form=form)

#home page super admin
@app.route('/super_admin_home')
@login_required
def super_admin_home():
    if not is_super_admin():
        flash("Access denied. Only super admins can access this page.", 'danger')
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    restaurants = conn.execute('SELECT * FROM Restaurant').fetchall()
    conn.close()
    return render_template('super_admin_home.html', restaurants=restaurants)

#edit reviews as super admin
@app.route('/admin/edit_review/<int:review_id>', methods=['GET','POST'])
@login_required
def admin_edit_review(review_id):
    if not is_super_admin():
        flash("Access denied. Only super admins can edit reviews.", 'danger')
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    review = conn.execute('SELECT * FROM Review WHERE ReviewID = ?', (review_id,)).fetchone()
    if not review:
        conn.close()
        flash("Review not found.", 'danger')
        return redirect(url_for('admin_manage_reviews'))
    
    form = EditReviewForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_rating = form.rating.data
        new_comment = form.comment.data
        try:
            conn.execute('''
                UPDATE Review
                SET Rating = ?, Comment = ?
                WHERE ReviewID = ?
            ''', (float(new_rating), new_comment, review_id))
            conn.commit()
            flash("Review updated successfully.", 'success')
            update_restaurant_rating(review['RestaurantID'])
        except Exception as e:
            flash("An error occurred while updating the review.", 'danger')
        finally:
            conn.close()
        return redirect(url_for('admin_manage_reviews'))
    
    form.rating.data = review['Rating']
    form.comment.data = review['Comment']
    conn.close()
    return render_template('admin_edit_review.html', form=form, review=review)

#show all orders from the logged in user
@app.route('/orders_all')
@login_required
def orders_all():
    conn = get_db_connection()
    orders = conn.execute('''
        SELECT Orders.*, Restaurant.Name as RestaurantName
        FROM Orders
        JOIN DishOrder ON Orders.OrderID = DishOrder.OrderID
        JOIN Dish ON DishOrder.DishID = Dish.DishID
        JOIN Menu ON Dish.MenuID = Menu.MenuID
        JOIN Restaurant ON Menu.RestaurantID = Restaurant.RestaurantID
        WHERE Orders.UserID = ?
        GROUP BY Orders.OrderID
        ORDER BY datetime(OrderDate) DESC
    ''', (current_user.id,)).fetchall()
    conn.close()
    return render_template('orders_overall.html', orders=orders)

#show all reviews from the logged in user
@app.route('/reviews_overall')
@login_required
def reviews_overall():
    conn = get_db_connection()
    reviews = conn.execute('''
        SELECT Name, DatePosted, Review.Rating, Comment
        FROM Review
        JOIN Restaurant ON Review.RestaurantID = Restaurant.RestaurantID
        WHERE UserID = ?
        ORDER BY datetime(DatePosted) DESC
    ''', (current_user.id,)).fetchall()
    conn.close()
    return render_template('reviews_overall.html', reviews=reviews)

#show all reservations from the logged in user
@app.route('/reservations_all')
@login_required
def reservations_all():
    conn = get_db_connection()
    reservations = conn.execute('''
        SELECT Reservation.*, Restaurant.Name as RestaurantName
        FROM Reservation
        JOIN Restaurant ON Reservation.RestaurantID = Restaurant.RestaurantID
        WHERE UserID = ?
        ORDER BY ReservationDate DESC, ReservationTime DESC
    ''', (current_user.id,)).fetchall()
    conn.close()
    return render_template('reservations_overall.html', reservations=reservations)

if __name__ == '__main__':
    app.run(debug=True)
