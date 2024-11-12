
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
(10, 'Pho Palet', '212 Sheets St', 'Las Vegas', 'NV', '57383', 'http://phopalet.com', 2.3, 'Vietnamese');


INSERT INTO Orders (OrderID, UserID, OrderDate, OrderTotal, DeliveryAddress) VALUES
(1, 1, '2024-10-20', 45.00, '123 Main St, San Francisco'),
(2, 2, '2024-10-21', 60.00, '456 Elm St, New York')
(3, 3, '2024-10-19', 60.00, '789 Neem St, Madison')
(4, 4, '2024-10-23', 60.00, '101 Juana St, Reno')
(5, 5, '2024-10-22', 60.00, '112 Wisto St, Sacremento')
(6, 6, '2024-10-25', 60.00, '134 Arizona St, Austin')
(7, 7, '2024-10-26', 60.00, '516 Goodwill St, Milpitas')
(8, 8, '2024-10-26', 60.00, '718 Nolin St, Miami')
(9, 9, '2024-10-28', 60.00, '920 Amelia St, Seattle')
(10, 10, '2024-10-31', 60.00, '212 Sheets St, Las Vegas');

INSERT INTO DishOrder (DishOrderID, OrderID, DishID, Quantity) VALUES
(1, 1, 1, 2),
(2, 2, 2, 1),
(3, 3, 3, 1),
(4, 4, 4, 1)
(5, 5, 5, 2),
(6, 6, 6, 1),
(7, 7, 7, 1),
(8, 8, 8, 1)
(9, 9, 9, 1),
(10, 10, 10, 1);
INSERT INTO Review (ReviewID, UserID, RestaurantID, Rating, Comment, DatePosted) VALUES
(1, 1, 1, 4.5, 'Delicious pasta!', '2024-11-10'),
(2, 2, 2, 4.8, 'Amazing sushi!', '2024-11-11'),
(3, 3, 3, 3.2, 'The naan could have been cooked a little more', '2024-11-11'),
(4, 4, 4, 4.3, 'Best tacos in town!', '2024-11-10'),
(5, 5, 5, 4.9, 'The shawarmas I can never forget!', '2024-11-11'),
(6, 6, 6, 2.0, 'Honestly, very mid pizza', '2024-11-11'),
(7, 7, 7, 5.0, 'The most authentic Korean cuisine ever!', '2024-11-10'),
(8, 8, 8, 4.8, 'The flavor is too good to be true!', '2024-11-11'),
(9, 9, 9, 3.5, 'The best fried chicken spot in Seattle!', '2024-11-11'),
(10, 10, 10, 1.3 'The worst pho I've ever tried', '2024-11-11');

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
