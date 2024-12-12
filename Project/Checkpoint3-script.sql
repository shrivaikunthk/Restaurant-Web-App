-- Schema
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
    UNIQUE(UserID, RestaurantID)  
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


-- User Queries
SELECT * FROM User WHERE UserID = ?;
SELECT * FROM User WHERE Email = ?;

-- Restaurant Queries
SELECT * FROM Restaurant WHERE RestaurantID = ?;
SELECT * FROM Restaurant;
SELECT * FROM Restaurant WHERE 1=1; 
SELECT Restaurant.* FROM Favorites JOIN Restaurant ON Favorites.RestaurantID = Restaurant.RestaurantID WHERE Favorites.UserID = ?;

-- Orders Queries
SELECT * FROM Orders WHERE UserID = ? ORDER BY datetime(OrderDate) DESC LIMIT 1;
SELECT Orders.*, Restaurant.Name as RestaurantName 
FROM Orders 
JOIN DishOrder ON Orders.OrderID = DishOrder.OrderID 
JOIN Dish ON DishOrder.DishID = Dish.DishID 
JOIN Menu ON Dish.MenuID = Menu.MenuID 
JOIN Restaurant ON Menu.RestaurantID = Restaurant.RestaurantID 
WHERE Orders.UserID = ? 
GROUP BY Orders.OrderID 
ORDER BY datetime(OrderDate) DESC;

-- DishOrder Queries
SELECT * FROM DishOrder WHERE OrderID = ?;

-- Review Queries
SELECT Restaurant.Name as RestaurantName 
FROM DishOrder 
JOIN Dish ON DishOrder.DishID = Dish.DishID 
JOIN Menu ON Dish.MenuID = Menu.MenuID 
JOIN Restaurant ON Menu.RestaurantID = Restaurant.RestaurantID 
WHERE DishOrder.OrderID = ? LIMIT 1;

SELECT Review.*, Restaurant.Name as RestaurantName 
FROM Review 
JOIN Restaurant ON Review.RestaurantID = Restaurant.RestaurantID 
WHERE Review.UserID = ? 
ORDER BY datetime(DatePosted) DESC LIMIT 1;

SELECT Review.*, User.Name 
FROM Review 
JOIN User ON Review.UserID = User.UserID 
WHERE Review.RestaurantID = ? 
ORDER BY datetime(DatePosted) DESC;

SELECT Review.*, User.Name as ReviewerName, Restaurant.Name as RestaurantName 
FROM Review 
JOIN User ON Review.UserID = User.UserID 
JOIN Restaurant ON Review.RestaurantID = Restaurant.RestaurantID 
ORDER BY datetime(DatePosted) DESC;

SELECT Name, DatePosted, Review.Rating, Comment 
FROM Review 
JOIN Restaurant ON Review.RestaurantID = Restaurant.RestaurantID 
WHERE UserID = ? 
ORDER BY datetime(DatePosted) DESC;

-- Reservation Queries
SELECT Reservation.*, Restaurant.Name as RestaurantName 
FROM Reservation 
JOIN Restaurant ON Reservation.RestaurantID = Restaurant.RestaurantID 
WHERE Reservation.UserID = ? 
  AND ReservationDate >= ? 
ORDER BY ReservationDate ASC, ReservationTime ASC LIMIT 1;

SELECT Reservation.*, User.Name as CustomerName 
FROM Reservation 
JOIN User ON Reservation.UserID = User.UserID 
WHERE Reservation.RestaurantID = ? 
ORDER BY ReservationDate DESC LIMIT ? OFFSET ?;

SELECT Reservation.*, User.Name as CustomerName, Restaurant.Name as RestaurantName 
FROM Reservation 
JOIN User ON Reservation.UserID = User.UserID 
JOIN Restaurant ON Reservation.RestaurantID = Restaurant.RestaurantID 
WHERE Reservation.RestaurantID = ? 
ORDER BY ReservationDate DESC LIMIT ? OFFSET ?;

SELECT * FROM Reservation WHERE ReservationID = ?;
SELECT * FROM Reservation WHERE RestaurantID = ? AND UserID = ? AND ReservationDate = ? AND ReservationTime = ?;
SELECT * FROM Reservation WHERE RestaurantID = ? AND UserID = ? AND ReservationDate = ? AND ReservationTime = ?;
SELECT * FROM Reservation WHERE RestaurantID = ? AND UserID = ? AND ReservationDate = ? AND ReservationTime = ?;

SELECT COUNT(*) FROM Reservation WHERE RestaurantID = ?;
SELECT COUNT(*) FROM Reservation;

SELECT * FROM Reservation WHERE ReservationID = ?;

-- Menu Queries
SELECT * FROM Menu WHERE RestaurantID = ?;
SELECT * FROM Menu WHERE MenuID = ?;
SELECT * FROM Menu WHERE RestaurantID = ?;
SELECT * FROM Menu WHERE RestaurantID = ?;

-- Dish Queries
SELECT * FROM Dish WHERE MenuID = ?;
SELECT * FROM Dish WHERE DishID = ?;
SELECT * FROM Dish WHERE DishID = ?;

-- Favorites Queries
SELECT * FROM Favorites WHERE UserID = ? AND RestaurantID = ?;
SELECT * FROM Favorites WHERE FavoriteID = ?;

-- Admin-Specific Queries
SELECT * FROM Restaurant WHERE RestaurantID = ?;
SELECT * FROM Menu WHERE MenuID = ?;
SELECT * FROM Menu WHERE RestaurantID = ?;
SELECT * FROM Dish WHERE MenuID = ?;
SELECT * FROM Menu WHERE MenuID = ?;
SELECT * FROM Restaurant WHERE RestaurantID = ?;
SELECT * FROM Review WHERE ReviewID = ?;

SELECT * FROM Restaurant;
SELECT * FROM Review WHERE ReviewID = ?;

SELECT * FROM User WHERE UserID = ?;


-- User Insertion
INSERT INTO User (Name, Email, Password, Phone, Location, Longitude, Latitude, Role) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?);

-- Review Insertion
INSERT INTO Review (UserID, RestaurantID, Rating, Comment, DatePosted) 
VALUES (?, ?, ?, ?, ?);

-- Reservation Insertion
INSERT INTO Reservation 
(UserID, RestaurantID, ReservationDate, ReservationTime, ReservationEndTime, NumberOfGuests, SpecialRequests) 
VALUES (?, ?, ?, ?, ?, ?, ?);

-- Favorites Insertion
INSERT INTO Favorites (UserID, RestaurantID) 
VALUES (?, ?);

-- Orders Insertion
INSERT INTO Orders (UserID, OrderDate, OrderTotal, DeliveryAddress) 
VALUES (?, ?, ?, ?);

INSERT INTO DishOrder (OrderID, DishID, Quantity) 
VALUES (?, ?, ?);

-- Menu Insertion
INSERT INTO Menu (RestaurantID, MenuName, Description) 
VALUES (?, ?, ?);

-- Dish Insertion
INSERT INTO Dish (MenuID, DishName, Description, Price) 
VALUES (?, ?, ?, ?);

-- Restaurant Insertion
INSERT INTO Restaurant 
(Name, Address, City, State, ZipCode, Website, CuisineType, Longitude, Latitude, NumberOfTables, MaxPeoplePerTable) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);

-- User Update
UPDATE User 
SET Name = ?, Email = ?, Phone = ?, Location = ?, Latitude = ?, Longitude = ? 
WHERE UserID = ?;

-- Restaurant Rating Update
UPDATE Restaurant 
SET Rating = ? 
WHERE RestaurantID = ?;

-- Reservation Update
UPDATE Reservation 
SET ReservationDate = ?, ReservationTime = ?, ReservationEndTime = ?, 
    NumberOfGuests = ?, SpecialRequests = ? 
WHERE ReservationID = ?;

-- Restaurant Update
UPDATE Restaurant 
SET Name = ?, Address = ?, City = ?, State = ?, ZipCode = ?, 
    Website = ?, Rating = ?, CuisineType = ?, Longitude = ?, 
    Latitude = ?, NumberOfTables = ?, MaxPeoplePerTable = ? 
WHERE RestaurantID = ?;

-- Menu Update
UPDATE Menu 
SET MenuName = ?, Description = ? 
WHERE MenuID = ?;

-- Dish Update
UPDATE Dish 
SET DishName = ?, Description = ?, Price = ? 
WHERE DishID = ?;

-- Review Update
UPDATE Review 
SET Rating = ?, Comment = ? 
WHERE ReviewID = ?;

-- Orders Update
UPDATE Orders 
SET OrderTotal = ? 
WHERE OrderID = ?;

-- Favorites Deletion
DELETE FROM Favorites 
WHERE FavoriteID = ?;

-- Review Deletion
DELETE FROM Review 
WHERE ReviewID = ?;

-- Reservation Deletion
DELETE FROM Reservation 
WHERE ReservationID = ?;

-- Menu Deletion
DELETE FROM Dish 
WHERE MenuID = ?;

DELETE FROM Menu 
WHERE MenuID = ?;

-- Dish Deletion
DELETE FROM Dish 
WHERE DishID = ?;
