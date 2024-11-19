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

### **Tables**
#### **Hotel**
| Column Name   | Data Type  | Constraints  |
|---------------|------------|--------------|
| hotel_id      | INT        | PRIMARY KEY  |
| hotel_name    | VARCHAR    | NOT NULL     |
| location      | VARCHAR    |              |

#### **Guest**
| Column Name   | Data Type  | Constraints  |
|---------------|------------|--------------|
| guest_id      | INT        | PRIMARY KEY  |
| guest_name    | VARCHAR    | NOT NULL     |
| phone_number  | VARCHAR    |              |

#### **Room**
| Column Name     | Data Type  | Constraints                                    |
|-----------------|------------|------------------------------------------------|
| room_id         | INT        | PRIMARY KEY                                    |
| room_type       | VARCHAR    | NOT NULL                                       |
| price           | DECIMAL    |                                                |
| room_condition  | VARCHAR    | CHECK (room_condition IN ('Clean', 'Dirty'))   |
| status          | VARCHAR    | CHECK (status IN ('Vacant', 'Occupied'))       |

#### **Booking**
| Column Name     | Data Type  | Constraints                        |
|-----------------|------------|------------------------------------|
| booking_id      | INT        | PRIMARY KEY                       |
| guest_id        | INT        | FOREIGN KEY REFERENCES Guest(guest_id) |
| room_id         | INT        | FOREIGN KEY REFERENCES Room(room_id)  |
| check_in_date   | DATE       | NOT NULL                          |
| check_out_date  | DATE       | NOT NULL                          |

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
    phone_number VARCHAR(15)
);

CREATE TABLE Room (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_type VARCHAR(50) NOT NULL,
    price DECIMAL(8, 2),
    room_condition VARCHAR(10),
    status VARCHAR(10)
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

## **Queries**

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

