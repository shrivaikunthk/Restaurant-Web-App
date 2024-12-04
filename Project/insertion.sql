
INSERT INTO Restaurant (RestaurantID, Name, Address, City, State, ZipCode, Website, Rating, CuisineType) VALUES
(1, 'Pasta Palace', '123 Main St', 'San Francisco', 'CA', '94105', 'http://pastapalace.com', 4.5, 'Italian'),
(2, 'Sushi World', '456 Elm St', 'New York', 'NY', '10001', 'http://sushiworld.com', 4.7, 'Japanese'),
(3, 'Desi Express', '789 Neem St', 'Madison', 'WI', '54900', 'http://desiexpress.com', 3.2, 'Indian'),
(4, 'Taco Land', '101 Juana St', 'Reno', 'NV', '34291', 'http://tacoland.com', 4.9, 'Mexican'),
(5, 'Shawarma Pointe', '112 Wisto St', 'Sacremento', 'CA', '94501', 'http://shawarmapointe.com', 4.5, 'Middle Eastern'),
(6, 'Joe's Pizza', '134 Arizona St', 'Austin', 'TX', '17848', 'http://joespizza.com', 3.4, 'American'),
(7, 'Kimchi Pot', '516 Goodwill St', 'Milpitas', 'CA', '95035', 'http://kimchipot.com', 5.0, 'Korean'),
(8, 'Cajun Kitchen', '718 Nolin St', 'Miami', 'FL', '68630', 'http://cajunkitchen.com', 4.2, 'American'),
(9, 'Chicken n' Go', '920 Amelia St', 'Seattle', 'WA', '45627', 'http://chickenngo.com', 4.7, 'American'),
(10, 'Pho Palate', '212 Sheets St', 'Las Vegas', 'NV', '57383', 'http://phopalet.com', 2.3, 'Vietnamese');


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