-- 14. Get details of users who have reserved more than 5 times
SELECT User.Name, User.Email, COUNT(*) AS TotalReservations
FROM User
JOIN Reservation ON User.UserID = Reservation.UserID
GROUP BY User.UserID HAVING TotalReservations > 5;
-- 19. Fetch all orders along with total amount spent by a user
SELECT OrderID, UserID, SUM(OrderTotal) AS TotalSpent 
FROM Orders 
WHERE UserID = 1 
GROUP BY OrderID;
-- 22. View users' special requests on their reservations
SELECT UserID, SpecialRequests 
FROM Reservation 
WHERE SpecialRequests IS NOT NULL;
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