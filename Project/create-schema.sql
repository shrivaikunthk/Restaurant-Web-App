-- Table for Users
CREATE TABLE User (
    UserID INTEGER PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    Password VARCHAR(100),
    Phone VARCHAR(15),
    Location VARCHAR(255)
);

-- Table for Restaurants
CREATE TABLE Restaurant (
    RestaurantID INTEGER PRIMARY KEY,
    Name VARCHAR(100),
    Address VARCHAR(255),
    City VARCHAR(100),
    State VARCHAR(50),
    ZipCode VARCHAR(10),
    Website VARCHAR(255),
    Rating DOUBLE,
    CuisineType VARCHAR(50)
);

-- Table for Orders
CREATE TABLE Orders (
    OrderID INTEGER PRIMARY KEY,
    UserID INT,
    OrderDate DATETIME,
    OrderTotal DOUBLE,
    DeliveryAddress VARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

-- Table for DishOrder (junction table between Order and Dish)
CREATE TABLE DishOrder (
    DishOrderID INTEGER PRIMARY KEY,
    OrderID INT,
    DishID INT,
    Quantity INT,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (DishID) REFERENCES Dish(DishID)
);

-- Table for Reviews
CREATE TABLE Review (
    ReviewID INTEGER PRIMARY KEY,
    UserID INT,
    RestaurantID INT,
    Rating DOUBLE,
    Comment TEXT,
    DatePosted DATETIME,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID)
);

-- Table for Favorites (junction table between User and Restaurant)
CREATE TABLE Favorites (
    FavoriteID INTEGER PRIMARY KEY,
    UserID INT,
    RestaurantID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID)
);

-- Table for Reservations
CREATE TABLE Reservation (
    ReservationID INTEGER PRIMARY KEY,
    UserID INT,
    RestaurantID INT,
    ReservationDate DATE,
    ReservationTime TIME,
    NumberOfGuests INT,
    SpecialRequests VARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID)
);

-- Table for Menu
CREATE TABLE Menu (
    MenuID INTEGER PRIMARY KEY,
    RestaurantID INT,
    MenuName VARCHAR(100),
    Description TEXT,
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID)
);

-- Table for Dishes (associated with a Menu)
CREATE TABLE Dish (
    DishID INTEGER PRIMARY KEY,
    MenuID INT,
    DishName VARCHAR(100),
    Description TEXT,
    Price DOUBLE,
    FOREIGN KEY (MenuID) REFERENCES Menu(MenuID)
);
