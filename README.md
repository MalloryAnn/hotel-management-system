# **hotel-management-system**
database systems project


## **Table of Contents**
- [Introduction](#introduction)
- [Team Members](#team-members)
- [Purpose](#purpose)
- [Database Design](#database-design)
  - [Tables](#tables)
- [SQL Schema](#sql-schema)
- [Sample Data](#sample-data)
- [Queries](#queries)
- [Future Enhancements](#future-enhancements)

---

## **Introduction**
The **Hotel Management System** is a database-driven project designed to simplify hotel operations. It manages hotel bookings, room availability, and guest information efficiently using a structured relational database. The system is divided into four core tables to ensure clarity and functionality.

---

## **Team Members**
- **Adrian Lopez**  
- **Jose Valdespino**  
- **Demetrio Deanda**  
- **Mallory Sorola**  

---

## **Purpose**
This system:
- **Streamlines hotel operations** by organizing bookings and room management.
- **Optimizes room usage** by tracking availability and conditions.  
- **Enhances guest satisfaction** by maintaining accurate and accessible records.

Future features include:
- A **Graphical User Interface (GUI)** for easy interactions.  
- **Real-time updates** on room availability.  
- **Automated notifications** for bookings and check-ins.  

---

## **Database Design**

#### **Hotel**
| Column Name | Data Type | Constraints    |
|-------------|-----------|----------------|
| hotel_id    | INT       | PRIMARY KEY    |
| hotel_name  | VARCHAR   | NOT NULL       |
| location    | VARCHAR   |                |

#### **Guest**
| Column Name  | Data Type | Constraints       |
|--------------|-----------|-------------------|
| guest_id     | INT       | PRIMARY KEY       |
| guest_name   | VARCHAR   | NOT NULL          |
| phone_number | VARCHAR   | UNIQUE            |
| email        | VARCHAR   | UNIQUE (optional) |

#### **Room**
| Column Name    | Data Type   | Constraints                           |
|----------------|-------------|---------------------------------------|
| room_id        | INT         | PRIMARY KEY                          |
| room_type      | VARCHAR     | NOT NULL                             |
| price          | DECIMAL     | NOT NULL, CHECK (price > 0)          |
| room_condition | VARCHAR     | CHECK (room_condition IN ('Clean', 'Dirty')) |
| status         | VARCHAR     | NOT NULL, CHECK (status IN ('Vacant', 'Occupied')) |
| room_view      | VARCHAR     |                                       |
| amenities      | VARCHAR     |                                       |

#### **Booking**
| Column Name     | Data Type | Constraints               |
|-----------------|-----------|---------------------------|
| booking_id      | INT       | PRIMARY KEY               |
| guest_id        | INT       | FOREIGN KEY (Guest.guest_id) |
| room_id         | INT       | FOREIGN KEY (Room.room_id) |
| check_in_date   | DATE      | NOT NULL                  |
| check_out_date  | DATE      | NOT NULL                  |

---

## **SQL Schema**

### **Tables**

```sql
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
```
---

### **SQL Queries**

```sql
-- View all tables
SELECT * FROM Hotel;
SELECT * FROM Guest;
SELECT * FROM Room;
SELECT * FROM Booking;

-- Find available rooms
SELECT * FROM Room WHERE status = 'Vacant';

-- Revenue by room type
SELECT room_type, SUM(price) AS total_revenue
FROM Booking
JOIN Room ON Booking.room_id = Room.room_id
GROUP BY room_type;

-- Find guests with multiple bookings
SELECT guest_id, COUNT(*) AS booking_count
FROM Booking
GROUP BY guest_id
HAVING COUNT(*) > 1;

-- List bookings for a specific date range
SELECT * FROM Booking
WHERE check_in_date >= '2024-11-01' AND check_out_date <= '2024-12-31';

-- Find occupied rooms on a specific date
SELECT Room.room_id, room_type, status
FROM Room
JOIN Booking ON Room.room_id = Booking.room_id
WHERE '2024-11-13' BETWEEN check_in_date AND check_out_date;
```
---

## **Advanced SQL Queries**
### **Managing Room Availability**
```sql
-- Filters Rooms by Date Range and Availability

SELECT Room.room_id, room_type, price, room_condition, status
FROM Room
       LEFT JOIN Booking ON Room.room_id = Booking.room_id
WHERE (
  Booking.check_out_date < '2024-11-01' OR Booking.check_in_date > '2024-11-10'
    OR Booking.room_id IS NULL
  ) AND Room.status = 'Vacant';

--Filters Rooms by Type and Pricing

SELECT *
FROM Room
WHERE room_type = 'Deluxe' AND price BETWEEN 100 AND 200 AND status = 'Vacant';

--Find Rooms by Condition

SELECT *
FROM Room
WHERE room_condition = 'Good' AND status = 'Vacant';
```

### **Guest Insights**

```sql
-- Identify Repeat Customers

SELECT Guest.guest_id, guest_name, COUNT(Booking.booking_id) AS booking_count
FROM Guest
       JOIN Booking ON Guest.guest_id = Booking.guest_id
GROUP BY Guest.guest_id
HAVING COUNT(Booking.booking_id) > 1;

-- Retrieve Guest History

SELECT Guest.guest_id, guest_name, phone_number, Booking.booking_id, check_in_date, check_out_date, Room.room_type
FROM Guest
       JOIN Booking ON Guest.guest_id = Booking.guest_id
       JOIN Room ON Booking.room_id = Room.room_id
WHERE Guest.guest_id = 1; -- Replace 1 with the desired guest ID
```

### Booking Analytics

```sql
-- Calculate Total Revenue by Room Type

SELECT Room.room_type, SUM(Room.price * DATEDIFF(Booking.check_out_date, Booking.check_in_date)) AS total_revenue
FROM Booking
       JOIN Room ON Booking.room_id = Room.room_id
GROUP BY Room.room_type;

-- Calculate Occupancy Rates

SELECT Room.room_type,
       COUNT(Booking.room_id) AS bookings_count,
       ROUND(COUNT(Booking.room_id) / (SELECT COUNT(*) FROM Room) * 100, 2) AS occupancy_rate
FROM Booking
       JOIN Room ON Booking.room_id = Room.room_id
GROUP BY Room.room_type;

-- Identify Underutilized Rooms

SELECT Room.room_id, room_type, COUNT(Booking.booking_id) AS bookings_count
FROM Room
       LEFT JOIN Booking ON Room.room_id = Booking.room_id
GROUP BY Room.room_id, room_type
HAVING COUNT(Booking.booking_id) < 2; -- Rooms booked less than twice
```
### Integration and Testing

```sql
-- Testing for Room Availability

SELECT Room.room_id, room_type, price, room_condition, status
FROM Room
WHERE status = 'Vacant';

-- Verifying Revenue Calculations

SELECT Room.room_type, SUM(price) AS total_revenue
FROM Booking
       JOIN Room ON Booking.room_id = Room.room_id
GROUP BY Room.room_type;


-- Testing Booking Insights 

SELECT Booking.booking_id, Guest.guest_name, Room.room_type, check_in_date, check_out_date
FROM Booking
       JOIN Guest ON Booking.guest_id = Guest.guest_id
       JOIN Room ON Booking.room_id = Room.room_id
WHERE check_in_date >= '2024-11-01' AND check_out_date <= '2024-12-31';
```


