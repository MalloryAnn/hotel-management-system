USE HotelManagementSystem;

CREATE TABLE Hotel (
    hotel_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_name VARCHAR(100) NOT NULL,
    location VARCHAR(100)
);

CREATE TABLE Guest (
    guest_id INT AUTO_INCREMENT PRIMARY KEY,
    guest_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(15),
    email VARCHAR(255),
    CONSTRAINT UNIQUE (phone_number),
    CONSTRAINT UNIQUE (email)
);
CREATE TABLE Room (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_type VARCHAR(50) NOT NULL,
    price DECIMAL(8, 2) NOT NULL CHECK (price > 0),
    room_condition VARCHAR(10) CHECK (room_condition IN ('Clean', 'Dirty')),
    status VARCHAR(10) NOT NULL CHECK (status IN ('Vacant', 'Occupied')),
    room_view VARCHAR(50),
    amenities VARCHAR(255)
);
CREATE TABLE Booking (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    guest_id INT,
    room_id INT,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    FOREIGN KEY (guest_id) REFERENCES Guest(guest_id),
    FOREIGN KEY (room_id) REFERENCES Room(room_id)
);

INSERT INTO Room (room_type, price, room_condition, status, room_view, amenities)
VALUES 
('Single', 120.00, 'Clean', 'Vacant', 'Sea View', 'WiFi, AC'),
('Double', 200.00, 'Dirty', 'Occupied', 'City View', 'WiFi, TV, Mini-bar'),
('Suite', 350.00, 'Clean', 'Vacant', 'Ocean View', 'WiFi, AC, Jacuzzi');

INSERT INTO Guest (guest_name, phone_number, email)
VALUES
('John Doe', '1234567890', 'john.doe@example.com'),
('Jane Smith', '0987654321', 'jane.smith@example.com');

INSERT INTO Booking (guest_id, room_id, check_in_date, check_out_date)
VALUES
(1, 1, '2024-12-01', '2024-12-05'),
(2, 2, '2024-12-10', '2024-12-15'),
(1, 3, '2024-12-05', '2024-12-08'); -- Overlapping booking

SELECT b1.booking_id, b1.room_id, b1.check_in_date, b1.check_out_date
FROM Booking b1, Booking b2
WHERE b1.room_id = b2.room_id 
  AND b1.booking_id != b2.booking_id
  AND b1.check_in_date < b2.check_out_date
  AND b1.check_out_date > b2.check_in_date;

INSERT INTO Room (room_type, price, room_condition, status, room_view, amenities)
VALUES 
('Single', 100.00, 'Clean', 'Vacant', 'Garden View', 'WiFi, TV'),
('Double', 150.00, 'Clean', 'Vacant', 'Sea View', 'WiFi, AC, Mini-bar'),
('Suite', 400.00, 'Clean', 'Occupied', 'Ocean View', 'WiFi, AC, Jacuzzi, Kitchenette'),
('Penthouse', 800.00, 'Clean', 'Vacant', 'City Skyline', 'WiFi, AC, Private Pool'),
('Family', 300.00, 'Dirty', 'Occupied', 'Park View', 'WiFi, AC, Baby Crib, TV'),
('Single', 120.00, 'Clean', 'Vacant', 'City View', 'WiFi, AC'),
('Double', 180.00, 'Clean', 'Occupied', 'Mountain View', 'WiFi, AC, Mini-bar'),
('Suite', 500.00, 'Clean', 'Vacant', 'Ocean View', 'WiFi, Jacuzzi, Private Balcony');

INSERT INTO Guest (guest_name, phone_number, email)
VALUES
('Emily Rose', '9876543210', 'emily.rose@example.com'),
('Michael Johnson', '5551112233', 'michael.johnson@example.com'),
('Sarah Connor', '5553334444', 'sarah.connor@example.com'),
('Peter Parker', '5557778888', 'peter.parker@example.com'),
('Tony Stark', '5550009999', 'tony.stark@example.com'),
('Natasha Romanoff', '5551234567', 'natasha.romanoff@example.com'),
('Bruce Wayne', '5559876543', 'bruce.wayne@example.com'),
('Diana Prince', '5552468101', 'diana.prince@example.com');

INSERT INTO Booking (guest_id, room_id, check_in_date, check_out_date)
VALUES
(3, 4, '2024-12-01', '2024-12-03'),
(4, 2, '2024-12-02', '2024-12-06'),
(5, 3, '2024-12-05', '2024-12-09'),
(6, 5, '2024-12-07', '2024-12-10'),
(7, 1, '2024-12-08', '2024-12-12'),
(8, 6, '2024-12-11', '2024-12-15'),
(1, 7, '2024-12-13', '2024-12-17'),
(2, 8, '2024-12-15', '2024-12-18');

SELECT b1.booking_id, b1.room_id, b1.check_in_date, b1.check_out_date
FROM Booking b1, Booking b2
WHERE b1.room_id = b2.room_id 
  AND b1.booking_id != b2.booking_id
  AND b1.check_in_date < b2.check_out_date
  AND b1.check_out_date > b2.check_in_date;

ALTER TABLE Room AUTO_INCREMENT = 100;
