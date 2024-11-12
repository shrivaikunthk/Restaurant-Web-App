
INSERT INTO Restaurant (RestaurantID, Name, Address, City, State, ZipCode, Website, Rating, CuisineType) VALUES
(1, 'Pasta Palace', '123 Main St', 'San Francisco', 'CA', '94105', 'http://pastapalace.com', 4.5, 'Italian'),
(2, 'Sushi World', '456 Elm St', 'New York', 'NY', '10001', 'http://sushiworld.com', 4.7, 'Japanese');

INSERT INTO Orders (OrderID, UserID, OrderDate, OrderTotal, DeliveryAddress) VALUES
(1, 1, '2024-10-20', 45.00, '123 Main St, San Francisco'),
(2, 2, '2024-10-21', 60.00, '456 Elm St, New York');

INSERT INTO DishOrder (DishOrderID, OrderID, DishID, Quantity) VALUES
(1, 1, 1, 2),
(2, 2, 2, 1);

INSERT INTO Review (ReviewID, UserID, RestaurantID, Rating, Comment, DatePosted) VALUES
(1, 1, 1, 4.5, 'Delicious pasta!', '2024-11-10'),
(2, 2, 2, 4.8, 'Amazing sushi!', '2024-11-11');

INSERT INTO Favorites (FavoriteID, UserID, RestaurantID) VALUES
(1, 1, 1),
(2, 2, 2);

INSERT INTO Reservation (ReservationID, UserID, RestaurantID, ReservationDate, ReservationTime, NumberOfGuests, SpecialRequests) VALUES
(1, 1, 1, '2024-11-15', '18:00:00', 4, 'Window seat'),
(2, 2, 2, '2024-11-16', '19:00:00', 2, 'Quiet area');

INSERT INTO Menu (MenuID, RestaurantID, MenuName, Description) VALUES
(1, 1, 'Dinner Menu', 'Our finest selection of Italian cuisine'),
(2, 2, 'Lunch Menu', 'Delicious Japanese specialties');

INSERT INTO Dish (DishID, MenuID, DishName, Description, Price) VALUES
(1, 1, 'Spaghetti Carbonara', 'Classic Italian pasta dish', 15.00),
(2, 2, 'Salmon Sushi', 'Fresh salmon on rice', 12.00);

-- INSERT INTO Review (ReviewID, UserID, RestaurantID, Rating, Comment, DatePosted) VALUES
-- (3, 1, 1, 4.5, 'WOW FOOD IG!', '2024-11-10');