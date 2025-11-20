"""
Smart Bike Database Setup Script
Run once to create and populate database with all data

Usage:
  python setup_database.py
"""

import mysql.connector
from werkzeug.security import generate_password_hash
import sys

# Database configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""  # Leave blank for XAMPP default, change if you set a password
DB_NAME = "smart_bike_db"

print("🔄 Connecting to MySQL...")

try:
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS)
except Exception as e:
    print(f"❌ Error connecting to MySQL: {e}")
    print("Make sure XAMPP MySQL is running!")
    sys.exit(1)

cur = conn.cursor()

# Create database
print("📦 Creating database...")
cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
cur.execute(f"USE {DB_NAME}")

# Create tables
print("🗂️  Creating tables...")

cur.execute("""
CREATE TABLE IF NOT EXISTS bicycles (
  bike_id INT PRIMARY KEY,
  qr_code VARCHAR(50) UNIQUE NOT NULL,
  is_available TINYINT(1) DEFAULT 1,
  location VARCHAR(255) NOT NULL,
  status VARCHAR(50) NOT NULL
) ENGINE=InnoDB;
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(150) UNIQUE,
  password VARCHAR(255),
  wallet_balance FLOAT DEFAULT 0
) ENGINE=InnoDB;
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS rides (
  id INT AUTO_INCREMENT PRIMARY KEY,
  ride_id INT NOT NULL,
  bike_id INT NOT NULL,
  start_time DATETIME NOT NULL,
  end_time DATETIME NOT NULL,
  fare DECIMAL(7,2) NOT NULL,
  status VARCHAR(20) NOT NULL
) ENGINE=InnoDB;
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS transactions (
  txn_id INT AUTO_INCREMENT PRIMARY KEY,
  id INT NOT NULL,
  amount DECIMAL(9,2) NOT NULL,
  type VARCHAR(50) NOT NULL,
  created_at DATETIME NOT NULL
) ENGINE=InnoDB;
""")

print("✅ Tables created successfully!")

# Insert bicycles data (all 45 bikes)
print("🚲 Inserting bicycles data...")
bicycles_data = [
    (101, 'BIKE-QR-001', 1, 'Girls Hostel', 'idle'),
    (102, 'BIKE-QR-002', 0, 'SR Block', 'in_use'),
    (103, 'BIKE-QR-003', 1, 'Ganga/Vedavati Hostel', 'idle'),
    (104, 'BIKE-QR-004', 1, 'C.V. Raman Block', 'idle'),
    (105, 'BIKE-QR-005', 0, 'Football Ground', 'in_use'),
    (106, 'BIKE-QR-006', 1, 'Ganga/Vedavati Hostel', 'idle'),
    (107, 'BIKE-QR-007', 1, 'SR Block', 'idle'),
    (108, 'BIKE-QR-008', 0, 'Girls Hostel', 'in_use'),
    (109, 'BIKE-QR-009', 1, 'Football Ground', 'idle'),
    (110, 'BIKE-QR-010', 1, 'C.V. Raman Block', 'idle'),
    (111, 'BIKE-QR-011', 1, 'Ganga/Vedavati Hostel', 'idle'),
    (112, 'BIKE-QR-012', 0, 'SR Block', 'in_use'),
    (113, 'BIKE-QR-013', 1, 'Football Ground', 'idle'),
    (114, 'BIKE-QR-014', 1, 'Girls Hostel', 'idle'),
    (115, 'BIKE-QR-015', 0, 'C.V. Raman Block', 'in_use'),
    (116, 'BIKE-QR-016', 1, 'Girls Hostel', 'idle'),
    (117, 'BIKE-QR-017', 1, 'SR Block', 'idle'),
    (118, 'BIKE-QR-018', 0, 'C.V. Raman Block', 'in_use'),
    (119, 'BIKE-QR-019', 1, 'Football Ground', 'idle'),
    (120, 'BIKE-QR-020', 1, 'Ganga/Vedavati Hostel', 'idle'),
    (121, 'BIKE-QR-021', 0, 'Girls Hostel', 'in_use'),
    (122, 'BIKE-QR-022', 1, 'SR Block', 'idle'),
    (123, 'BIKE-QR-023', 1, 'C.V. Raman Block', 'idle'),
    (124, 'BIKE-QR-024', 0, 'Football Ground', 'in_use'),
    (125, 'BIKE-QR-025', 1, 'Ganga/Vedavati Hostel', 'idle'),
    (126, 'BIKE-QR-026', 1, 'Girls Hostel', 'idle'),
    (127, 'BIKE-QR-027', 0, 'SR Block', 'in_use'),
    (128, 'BIKE-QR-028', 1, 'C.V. Raman Block', 'idle'),
    (129, 'BIKE-QR-029', 1, 'Football Ground', 'idle'),
    (130, 'BIKE-QR-030', 0, 'Ganga/Vedavati Hostel', 'in_use'),
    (131, 'BIKE-QR-031', 1, 'Girls Hostel', 'idle'),
    (132, 'BIKE-QR-032', 1, 'SR Block', 'idle'),
    (133, 'BIKE-QR-033', 1, 'C.V. Raman Block', 'idle'),
    (134, 'BIKE-QR-034', 0, 'Football Ground', 'in_use'),
    (135, 'BIKE-QR-035', 1, 'Ganga/Vedavati Hostel', 'idle'),
    (136, 'BIKE-QR-036', 1, 'Girls Hostel', 'idle'),
    (137, 'BIKE-QR-037', 1, 'SR Block', 'idle'),
    (138, 'BIKE-QR-038', 0, 'C.V. Raman Block', 'in_use'),
    (139, 'BIKE-QR-039', 1, 'Football Ground', 'idle'),
    (140, 'BIKE-QR-040', 1, 'Ganga/Vedavati Hostel', 'idle'),
    (141, 'BIKE-QR-041', 1, 'Girls Hostel', 'idle'),
    (142, 'BIKE-QR-042', 0, 'SR Block', 'in_use'),
    (143, 'BIKE-QR-043', 1, 'C.V. Raman Block', 'idle'),
    (144, 'BIKE-QR-044', 1, 'Football Ground', 'idle'),
    (145, 'BIKE-QR-045', 0, 'Ganga/Vedavati Hostel', 'in_use')
]

cur.executemany("""
INSERT IGNORE INTO bicycles (bike_id, qr_code, is_available, location, status)
VALUES (%s, %s, %s, %s, %s)
""", bicycles_data)
print(f"✅ Inserted {len(bicycles_data)} bicycles!")

# Insert students data with HASHED passwords
print("👥 Inserting students data...")
students_plain = [
    (1, 'Aarav Sharma', 'aarav.s@example.com', 'password123', 25.5),
    (2, 'Aditi Singh', 'aditi.si@example.com', 'password124', 18.75),
    (3, 'Aryan Kumar', 'aryan.k@example.com', 'password125', 30),
    (4, 'Bhavna Patel', 'bhavna.p@example.com', 'password126', 12.2),
    (5, 'Chirag Gupta', 'chirag.g@example.com', 'password127', 45.1),
    (6, 'Diya Joshi', 'diya.j@example.com', 'password128', 8.5),
    (7, 'Esha Reddy', 'esha.r@example.com', 'password129', 22),
    (8, 'Gaurav Mehta', 'gaurav.m@example.com', 'password130', 15.6),
    (9, 'Hina Khan', 'hina.k@example.com', 'password131', 33.9),
    (10, 'Ishaan Verma', 'ishaan.v@example.com', 'password132', 10),
    (11, 'Jhanvi Sharma', 'jhanvi.s@example.com', 'password133', 28.3),
    (12, 'Kabir Das', 'kabir.d@example.com', 'password134', 17.4),
    (13, 'Kavya Nair', 'kavya.n@example.com', 'password135', 36.8),
    (14, 'Lakshya Singh', 'lakshya.si@example.com', 'password136', 9.99),
    (15, 'Manya Arora', 'manya.a@example.com', 'password137', 40),
    (16, 'Nikhil Bansal', 'nikhil.b@example.com', 'password138', 21.5),
    (17, 'Pooja Devi', 'pooja.d@example.com', 'password139', 14.25),
    (18, 'Rahul Yadav', 'rahul.y@example.com', 'password140', 29),
    (19, 'Riya Sharma', 'riya.sh@example.com', 'password141', 11.8),
    (20, 'Sagar Verma', 'sagar.v@example.com', 'password142', 38.6),
    (21, 'Tanya Rao', 'tanya.r@example.com', 'password143', 7.2),
    (22, 'Uday Prakash', 'uday.p@example.com', 'password144', 24.9),
    (23, 'Vidya Menon', 'vidya.m@example.com', 'password145', 16.5),
    (24, 'Vivek Khanna', 'vivek.k@example.com', 'password146', 31),
    (25, 'Zara Ali', 'zara.a@example.com', 'password147', 13),
    (26, 'Amit Shah', 'amit.sh@example.com', 'password148', 35.5),
    (27, 'Gargi Desai', 'gargi.d@example.com', 'password149', 20),
    (28, 'Harsh Singh', 'harsh.si@example.com', 'password150', 19.1),
    (29, 'Neha Joshi', 'neha.j@example.com', 'password151', 27.75),
    (30, 'Pranav Kumar', 'pranav.k@example.com', 'password152', 6.75)
]

# Hash passwords before inserting
students_data = []
for id, name, email, pwd, bal in students_plain:
    students_data.append((id, name, email, generate_password_hash(pwd), bal))

cur.executemany("""
INSERT IGNORE INTO students (id, name, email, password, wallet_balance)
VALUES (%s, %s, %s, %s, %s)
""", students_data)
print(f"✅ Inserted {len(students_data)} students with hashed passwords!")

# Insert rides data
print("🚴 Inserting rides data...")
rides_data = [
    (1, 1, 101, '2023-10-26 09:00:00', '2023-10-26 09:30:00', 10.00, 'completed'),
    (2, 2, 102, '2023-10-26 10:15:00', '2023-10-26 10:45:00', 10.00, 'completed'),
    (3, 3, 103, '2023-10-26 11:00:00', '2023-10-26 11:40:00', 15.00, 'completed'),
    (4, 4, 104, '2023-10-26 13:00:00', '2023-10-26 13:20:00', 10.00, 'completed'),
    (5, 5, 123, '2023-11-08 13:00:00', '2023-11-08 13:30:00', 10.00, 'completed')
]

cur.executemany("""
INSERT IGNORE INTO rides (id, ride_id, bike_id, start_time, end_time, fare, status)
VALUES (%s, %s, %s, %s, %s, %s, %s)
""", rides_data)
print(f"✅ Inserted {len(rides_data)} rides!")

# Insert transactions data
print("💰 Inserting transactions data...")
transactions_data = [
    (1, 1, 10.00, 'deposit', '2023-10-25 08:00:00'),
    (2, 1, -2.50, 'ride_fare', '2023-10-26 09:30:01'),
    (3, 2, 5.00, 'deposit', '2023-10-25 09:00:00'),
    (4, 2, -3.00, 'ride_fare', '2023-10-26 10:45:01'),
    (5, 3, 15.00, 'deposit', '2023-10-25 10:00:00'),
    (6, 3, -3.50, 'ride_fare', '2023-10-26 11:40:01'),
    (7, 4, 7.00, 'deposit', '2023-10-25 11:00:00'),
    (8, 4, -2.00, 'ride_fare', '2023-10-26 13:20:01'),
    (9, 5, 20.00, 'deposit', '2023-10-25 12:00:00'),
    (10, 5, -4.00, 'ride_fare', '2023-10-26 14:50:01')
]

cur.executemany("""
INSERT IGNORE INTO transactions (txn_id, id, amount, type, created_at)
VALUES (%s, %s, %s, %s, %s)
""", transactions_data)
print(f"✅ Inserted {len(transactions_data)} transactions!")

# Commit and close
conn.commit()
cur.close()
conn.close()

print("\n" + "="*60)
print("🎉 DATABASE SETUP COMPLETE!")
print("="*60)
print(f"✅ Database: {DB_NAME}")
print(f"✅ Tables: bicycles, students, rides, transactions")
print(f"✅ {len(bicycles_data)} bikes")
print(f"✅ {len(students_data)} students (passwords hashed)")
print(f"✅ {len(rides_data)} rides")
print(f"✅ {len(transactions_data)} transactions")
print("\n📝 Next steps:")
print("1. Run: python generate_qr.py  (to create QR images)")
print("2. Run: python app.py          (to start your website)")
print("3. Open: http://localhost:5000")
print("="*60)
