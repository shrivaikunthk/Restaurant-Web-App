
-- 1. Retrieve all restaurants by city to display all restaurants when they are searching
SELECT Name, Address, City, State, Rating FROM Restaurant WHERE City = 'San Francisco';

-- 2. List all dishes for a given menu to show the menu
SELECT DishName, Description, Price FROM Dish WHERE MenuID = 1;

-- 3. Get all the ratings 
SELECT Rating, Comment, DatePosted FROM Review WHERE RestaurantID = 2;

-- 4. Average ratings
SELECT RestaurantID, AVG(Rating) AS AverageRating FROM Review GROUP BY RestaurantID;

-- 5. Inserting review (could use an auto-incrementer for ID will update later)
INSERT INTO Review (ReviewID, UserID, RestaurantID, Rating, Comment, DatePosted) VALUES
(3, 1, 1, 5, 'The food was amazing. I would recommend this place fosho fosho.', '2024-11-11');


-- 6. Deleting review
DELETE FROM Review WHERE ReviewID = 3;

-- 7. User info for reservation
SELECT User.Name, Reservation.ReservationDate, Reservation.ReservationTime, Reservation.NumberOfGuests, Reservation.SpecialRequests
FROM User
JOIN Reservation ON User.UserID = Reservation.UserID
WHERE Reservation.RestaurantID = 2;

-- 8. Fetch all reservations for a specific restaurant
SELECT UserID, ReservationDate, ReservationTime, NumberOfGuests, SpecialRequests FROM Reservation WHERE RestaurantID = 1;

-- 9. Update Reservation 
UPDATE Reservation
SET ReservationTime = '19:30:00', SpecialRequests = 'Quiet area', NumberOfGuests = 3
WHERE ReservationID = 2;

-- 10. Delete Reservation 
DELETE FROM Reservation
WHERE ReservationID = 3;

-- 11. Adding dishes to your order
INSERT INTO DishOrder (DishOrderID, OrderID, DishID, Quantity) VALUES (3, 2, 1, 2);

-- 12. List dishes ordered in a specific order
SELECT Dish.DishName, DishOrder.Quantity
FROM DishOrder
JOIN Dish ON DishOrder.DishID = Dish.DishID
WHERE OrderID = 2;

-- 13. Deleting dishes from your order
DELETE FROM DishOrder WHERE DishOrderID = 3 AND DishID = 1;


-- 14. View Favorites restaurants of a user
SELECT Restaurant.Name, Restaurant.City FROM Favorites
JOIN Restaurant ON Favorites.RestaurantID = Restaurant.RestaurantID
WHERE Favorites.UserID = 1;

-- 15. Inserting a user's favorited restaurant
INSERT INTO Favorites (FavoriteID, UserID, RestaurantID) VALUES (3, 1, 2);

-- 16. Delete a favorited restaurant
DELETE FROM Favorites WHERE UserID = 1 AND RestaurantID = 2;

-- 17. Get all users who reviewed a specific restaurant
SELECT User.Name, Review.Rating, Review.Comment
FROM Review
JOIN User ON Review.UserID = User.UserID
WHERE RestaurantID = 2;

-- 18. Editing a user review 
UPDATE Review
SET Rating = 4.0, Comment = 'I love the food but there was a long wait'
WHERE ReviewID = 3;

-- 19. Count total reviews per restaurant
SELECT Name, COUNT(*) AS TotalReviews FROM 
Review 
JOIN Restaurant ON Review.RestaurantID = Restaurant.RestaurantID
GROUP BY Name;

-- 20. Find all orders by a user within a specific date range
SELECT OrderID, OrderDate, OrderTotal FROM Orders
WHERE UserID = 2 AND OrderDate BETWEEN '2024-01-01' AND '2024-12-31';

-- 21. Show dishes in a user's recent order
SELECT Dish.DishName, DishOrder.Quantity
FROM Orders
JOIN DishOrder ON Orders.OrderID = DishOrder.OrderID
JOIN Dish ON DishOrder.DishID = Dish.DishID
WHERE Orders.UserID = 2 ORDER BY OrderDate DESC LIMIT 1;



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





-- 16. Display the average price of dishes in each menu
SELECT MenuID, AVG(Price) AS AveragePrice FROM Dish GROUP BY MenuID;

-- 17. List upcoming reservations for a specific restaurant
SELECT UserID, ReservationDate, ReservationTime, NumberOfGuests
FROM Reservation
WHERE RestaurantID = 1 AND ReservationDate > CURRENT_DATE;

-- 18. Show all Favorites restaurants with an average rating over 4
SELECT Restaurant.Name, AVG(Review.Rating) AS AverageRating
FROM Restaurant
JOIN Favorites ON Restaurant.RestaurantID = Favorites.RestaurantID
JOIN Review ON Restaurant.RestaurantID = Review.RestaurantID
GROUP BY Restaurant.RestaurantID HAVING AverageRating > 4;

-- 19. Fetch all orders along with total amount spent by a user
SELECT UserID, SUM(OrderTotal) AS TotalSpent FROM Orders WHERE UserID = 5;

-- 20. Retrieve all available dishes with a price under a certain amount
SELECT DishName, Price FROM Dish WHERE Price < 15;

-- 21. List the most popular restaurants based on Favoritess
SELECT RestaurantID, COUNT(*) AS FavoritesCount
FROM Favoritess
GROUP BY RestaurantID ORDER BY FavoritesCount DESC LIMIT 5;

-- 22. View users' special requests on their reservations
SELECT UserID, SpecialRequests FROM Reservation WHERE SpecialRequests IS NOT NULL;

-- 23. Get the total number of orders for each dish
SELECT DishID, SUM(Quantity) AS TotalOrdered FROM DishOrder GROUP BY DishID;

-- 24. Identify highly-rated restaurants for a specific cuisine
SELECT Name, Rating FROM Restaurant WHERE CuisineType = 'Italian' AND Rating > 4;

-- 25. Fetch all reviews and ratings left by a specific user
SELECT RestaurantID, Rating, Comment FROM Review WHERE UserID = 5;

-- 26. Show all reservations for a particular date
SELECT * FROM Reservation WHERE ReservationDate = '2024-11-15';

-- 27. Retrieve a list of dishes ordered more than 10 times
SELECT Dish.DishName, SUM(DishOrder.Quantity) AS TotalOrdered
FROM DishOrder
JOIN Dish ON DishOrder.DishID = Dish.DishID
GROUP BY Dish.DishID HAVING TotalOrdered > 10;

-- 28. Fetch restaurants with no reviews
SELECT Restaurant.Name FROM Restaurant
LEFT JOIN Review ON Restaurant.RestaurantID = Review.RestaurantID
WHERE Review.RestaurantID IS NULL;

-- 29. List all users who placed orders with a total over $50
SELECT UserID, OrderID, OrderTotal FROM Orders WHERE OrderTotal > 50;

-- 30. Retrieve the highest-priced dishes per menu
SELECT MenuID, DishID, MAX(Price) AS HighestPricedDish FROM Dish GROUP BY MenuID;

-- 31. Count total reservations made by a user
SELECT COUNT(*) AS totalRes FROM Reservation WHERE UserID = 2;

-- 14. Get details of users who have reserved more than 5 times
SELECT User.Name, User.Email, COUNT(*) AS TotalReservations
FROM User
JOIN Reservation ON User.UserID = Reservation.UserID
GROUP BY User.UserID HAVING TotalReservations > 5;