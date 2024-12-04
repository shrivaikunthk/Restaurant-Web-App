-- Insertion Queries for Data

DELETE FROM Restaurant;
INSERT INTO Restaurant ( Name, Address, City, State, ZipCode, Website, Rating, CuisineType,Longitude, Latitude) VALUES
( 'Pasta Palace', '123 Main St', 'San Francisco', 'CA', '94105', 'http://pastapalace.com', 4.5, 'Italian',-122.42,37.77),
('Sushi World', '456 Elm St', 'New York', 'NY', '10001', 'http://sushiworld.com', 4.7, 'Japanese',-74.00,40.71),
('Desi Express', '789 Neem St', 'Madison', 'WI', '54900', 'http://desiexpress.com', 3.2, 'Indian',-89.40,43.07),
('Taco Land', '101 Juana St', 'Reno', 'NV', '34291', 'http://tacoland.com', 4.9, 'Mexican',-119.81,39.53),
('Shawarma Pointe', '112 Wisto St', 'Sacramento', 'CA', '94501', 'http://shawarmapointe.com', 4.5, 'Middle Eastern',-121.49,38.58),
('Joes Pizza', '134 Arizona St', 'Austin', 'TX', '17848', 'http://joespizza.com', 3.4, 'American',-97.74,30.27),
('Kimchi Pot', '516 Goodwill St', 'Milpitas', 'CA', '95035', 'http://kimchipot.com', 5.0, 'Korean',-121.89,37.43),
('Cajun Kitchen', '718 Nolin St', 'Miami', 'FL', '68630', 'http://cajunkitchen.com', 4.2, 'American',-80.19,25.77),
('Chicken nGo', '920 Amelia St', 'Seattle', 'WA', '45627', 'http://chickenngo.com', 4.7, 'American',-122.33,47.60),
('Pho Palate', '212 Sheets St', 'Las Vegas', 'NV', '57383', 'http://phopalet.com', 2.3, 'Vietnamese',-115.15,36.17);

SELECT * FROM Restaurant;

INSERT INTO Orders ( UserID, OrderDate, OrderTotal, DeliveryAddress) VALUES
( 1, '2024-10-20', 45.00, '123 Main St, San Francisco'),
( 2, '2024-10-21', 60.00, '456 Elm St, New York'),
( 3, '2024-10-19', 90.00, '789 Neem St, Madison'),
( 4, '2024-10-23', 30.00, '101 Juana St, Reno'),
( 5, '2024-10-22', 40.00, '112 Wisto St, Sacremento'),
( 6, '2024-10-25', 50.00, '134 Arizona St, Austin'),
(7, '2024-10-26', 60.00, '516 Goodwill St, Milpitas'),
(8, '2024-10-26', 75.00, '718 Nolin St, Miami'),
( 9, '2024-10-28', 30.00, '920 Amelia St, Seattle'),
( 10, '2024-10-31', 80.00, '212 Sheets St, Las Vegas');

INSERT INTO DishOrder ( OrderID, DishID, Quantity) VALUES
( 1, 1, 2),
( 2, 2, 1),
( 3, 3, 1),
( 4, 4, 1),
( 5, 5, 2),
( 6, 6, 1),
( 7, 7, 1),
( 8, 8, 1),
( 9, 9, 1),
( 10, 10, 1);
INSERT INTO Review ( UserID, RestaurantID, Rating, Comment, DatePosted) VALUES
( 1, 1, 4.5, 'Delicious pasta!', '2024-11-10'),
( 2, 2, 4.8, 'Amazing sushi!', '2024-11-11'),
( 3, 3, 3.2, 'The naan could have been cooked a little more', '2024-11-11'),
( 4, 4, 4.3, 'Best tacos in town!', '2024-11-10'),
( 5, 5, 4.9, 'The shawarmas I can never forget!', '2024-11-11'),
( 6, 6, 2.0, 'Honestly, very mid pizza', '2024-11-11'),
( 7, 7, 5.0, 'The most authentic Korean cuisine ever!', '2024-11-10'),
(8, 8, 4.8, 'The flavor is too good to be true!', '2024-11-11'),
( 9, 9, 3.5, 'The best fried chicken spot in Seattle!', '2024-11-11'),
( 10, 10, 1.3 , 'The worst pho I have ever tried', '2024-11-11');

INSERT INTO Favorites ( UserID, RestaurantID) VALUES
( 1, 1),
(2, 2),
( 3, 3),
( 4, 4),
( 5, 5),
( 6, 6),
( 7, 7),
( 8, 8),
( 9, 9),
( 10, 10);

INSERT INTO Reservation ( UserID, RestaurantID, ReservationDate, ReservationTime, NumberOfGuests, SpecialRequests) VALUES
( 1, 1, '2024-11-15', '18:00:00', 4, 'Window seat'),
( 2, 2, '2024-11-16', '19:00:00', 2, 'Quiet area'),
( 3, 3, '2024-11-15', '18:00:00', 7, 'Big table'),
( 4, 4, '2024-11-16', '19:00:00', 2, 'Corner table'),
( 5, 5, '2024-11-15', '18:00:00', 4, 'Window seat'),
( 6, 6, '2024-11-16', '19:00:00', 2, 'Private area'),
( 7, 7, '2024-11-15', '18:00:00', 4, 'Booth'),
( 8, 8, '2024-11-16', '19:00:00', 2, 'Quiet area'),
(9, 9, '2024-11-15', '18:00:00', 4, 'Window seat'),
(10, 10, '2024-11-16', '19:00:00', 2, 'Quiet area');

INSERT INTO User(Name,Email,Password,Phone, Location) VALUES
('Shri', 'sk@gmai.com','******','9082412654', 'merced'),
('Kal', 'ka@gmail.com', '*****', '4085679697', 'fremont'),
('Bob', 'b@gmail.com','******', '765432876', 'dallas'),
('Alice','a@gmail.com','******','567898765', 'new jersey');

INSERT INTO Menu ( RestaurantID, MenuName, Description) VALUES
( 1, 'Dinner Menu', 'Our finest selection of Italian cuisine'),
( 2, 'Lunch Menu', 'Delicious Japanese specialties'),
( 3, 'Dinner Menu', 'Authentic Indian selections'),
( 4, 'Lunch Menu', 'Best tacos compilations'),
( 5, 'Dinner Menu', 'Flavorful blast of Shawarmas'),
( 6, 'Lunch Menu', 'Delicious Pizzas'),
( 7, 'Dinner Menu', 'Korean delicacies'),
( 8, 'Lunch Menu', 'Spiciest and mouthwatering specials'),
( 9, 'Dinner Menu', 'Chickens of all kinds'),
(10, 'Lunch Menu', 'Treat for your palate');

INSERT INTO Dish ( MenuID, DishName, Description, Price) VALUES
( 1, 'Spaghetti Carbonara', 'Classic Italian pasta dish', 15.00),
( 2, 'Salmon Sushi', 'Fresh salmon on rice', 12.00),
( 3, 'Butter Chicken and Naan', 'Classic Indian cuisine', 20.00),
( 4, 'Beef Tacos', 'Ten Beef Tacos served with cilantro and onions', 10.00),
( 5, 'Falafel', 'Classic Meditterean wrap with chicken', 18.00),
( 6, 'Meat Lovers', 'Three meat pizza with extra cheese', 20.00),
( 7, 'Carbonara Ttebokki', 'Classic Korean rice cake dish', 25.00),
( 8, 'Smoked Spicy Crab', 'Fresh crab marinated in cajun spices', 27.00),
( 9, 'Garlic Cheese Chicken', 'Fried Chicken with garlic seasoning and topped with cheese', 10.00),
( 10, 'Classic Pho', 'Chefs special pho with choice of meat', 30.00);


-- Actual Queries 
-- 1. Retrieve all restaurants by city to display all restaurants when they are searching
SELECT Name, Address, City, State, Rating 
FROM Restaurant 
WHERE City = 'San Francisco';

-- 2. List all dishes for a given menu to show the menu
SELECT DishName, Description, Price 
FROM Dish 
WHERE MenuID = 1;

-- 3. Get all the ratings 
SELECT Rating, Comment, DatePosted 
FROM Review 
WHERE RestaurantID = 2;

-- 4. Average ratings
SELECT RestaurantID, AVG(Rating) AS AverageRating 
FROM Review 
GROUP BY RestaurantID;

-- 5. Inserting review (could use an auto-incrementer for ID will update later)
INSERT INTO Review ( UserID, RestaurantID, Rating, Comment, DatePosted) VALUES
( 1, 1, 5, 'The food was amazing. I would recommend this place fosho fosho.', '2024-11-11');


-- 6. Deleting review
DELETE FROM Review 
WHERE ReviewID = 2;

-- 7. User info for reservation
SELECT User.Name, Reservation.ReservationDate, Reservation.ReservationTime, Reservation.NumberOfGuests, Reservation.SpecialRequests
FROM User
JOIN Reservation ON User.UserID = Reservation.UserID
WHERE Reservation.RestaurantID = 2;

-- 8. Fetch all reservations for a specific restaurant
SELECT UserID, ReservationDate, ReservationTime, NumberOfGuests, SpecialRequests 
FROM Reservation 
WHERE RestaurantID = 1;

-- 9. Update Reservation 
UPDATE Reservation
SET ReservationTime = '19:30:00', SpecialRequests = 'Quiet area', NumberOfGuests = 3
WHERE ReservationID = 2;

-- 10. Delete Reservation 
DELETE FROM Reservation
WHERE ReservationID = 3;

-- 11. Adding dishes to your order
INSERT INTO DishOrder (OrderID, DishID, Quantity) VALUES ( 2, 5, 2);

-- 12. List dishes ordered in a specific order
SELECT Dish.DishName, DishOrder.Quantity
FROM DishOrder
JOIN Dish ON DishOrder.DishID = Dish.DishID
WHERE OrderID = 2;

-- 13. Deleting dishes from your order
DELETE FROM DishOrder WHERE DishOrderID = 3 AND DishID = 1;

-- 14. View Favorites restaurants of a user
SELECT Restaurant.Name, Restaurant.City 
FROM Favorites
JOIN Restaurant ON Favorites.RestaurantID = Restaurant.RestaurantID
WHERE Favorites.UserID = 1;

-- 15. Inserting a user's favorited restaurant
INSERT INTO Favorites (UserID, RestaurantID) VALUES ( 1, 2);

-- 16. Delete a favorited restaurant
DELETE FROM Favorites 
WHERE UserID = 1 AND RestaurantID = 2;

-- 17. Get all users who reviewed a specific restaurant

SELECT User.Name, Review.Rating, Review.Comment
FROM Review
JOIN User ON Review.UserID = User.UserID
WHERE Review.RestaurantID = 1;

-- 18. Editing a user review 
UPDATE Review
SET Rating = 4.0, Comment = 'I love the food but there was a long wait'
WHERE ReviewID = 3;

-- 19. Count total reviews per restaurant
SELECT Name, COUNT(*) AS TotalReviews 
FROM Review 
JOIN Restaurant ON Review.RestaurantID = Restaurant.RestaurantID
GROUP BY Name;

-- 20. Find all orders by a user within a specific date range
SELECT OrderID, OrderDate, OrderTotal 
FROM Orders
WHERE UserID = 2 AND OrderDate BETWEEN '2024-01-01' AND '2024-12-31';

-- 21. Show dishes in a user's recent order
SELECT Dish.DishName, DishOrder.Quantity
FROM Orders
JOIN DishOrder ON Orders.OrderID = DishOrder.OrderID
JOIN Dish ON DishOrder.DishID = Dish.DishID
WHERE Orders.UserID = 2 
ORDER BY OrderDate 
DESC LIMIT 1;



-- 22. Retrieve the top-rated dish in the user's city 
SELECT Dish.DishName, Dish.Price, AVG(Review.Rating) AS AverageRating
FROM Dish
JOIN Menu ON Dish.MenuID = Menu.MenuID
JOIN Restaurant ON Menu.RestaurantID = Restaurant.RestaurantID
JOIN Review ON Restaurant.RestaurantID = Review.RestaurantID
JOIN User ON User.Location = Restaurant.City  --make sure restarurant is in the right city
WHERE User.UserID = 1 -- curent user
GROUP BY Dish.DishID
HAVING AverageRating > 4;


-- 23. Retrieve the top-rated dishes for a specific restaurant (e.g., RestaurantID = 1) with rating above 4
SELECT Dish.DishName, Dish.Price, AVG(Review.Rating) AS AverageRating
FROM Dish
JOIN Menu ON Dish.MenuID = Menu.MenuID
JOIN Review ON Menu.RestaurantID = Review.RestaurantID
WHERE Menu.RestaurantID = 1  -- restaurant ID
GROUP BY Dish.DishID
HAVING AverageRating > 4;

-- 24. Display the cheapest dish in each menu (could be all or j a select restaurant)
SELECT MenuID, MIN(Price) AS Cheapest 
FROM Dish 
GROUP BY MenuID;

-- 25. List upcoming reservations for a specific restaurant so they can whats open and not
SELECT UserID, ReservationDate, ReservationTime, NumberOfGuests
FROM Reservation
WHERE RestaurantID = 1 AND ReservationDate > CURRENT_DATE;

-- 26. Retrieve all available dishes with a price under a certain amount from a certian menu
SELECT DishName, Price 
FROM Dish 
WHERE MenuID = 2 AND Price < 15;

-- 27. List the most popular restaurants based on Favoritess
SELECT Name, COUNT(*) AS FavoritesCount
FROM Favorites
JOIN Restaurant ON Favorites.RestaurantID = Restaurant.RestaurantID
GROUP BY Name 
ORDER BY FavoritesCount 
DESC LIMIT 5;

-- 28. Get the total number of orders for each dish
SELECT DishID, SUM(Quantity) AS TotalOrdered 
FROM DishOrder 
GROUP BY DishID;

-- 29. Find highly-rated restaurants for a specific cuisine
SELECT Name, Rating 
FROM Restaurant 
WHERE CuisineType = 'Italian' AND Rating > 4;

-- 30. Get all reviews and ratings left by a specific user
SELECT RestaurantID, Rating, Comment 
FROM Review 
WHERE UserID = 1;

-- 31. Count total reservations made by a user
SELECT COUNT(*) AS totalRes 
FROM Reservation 
WHERE UserID = 2;

