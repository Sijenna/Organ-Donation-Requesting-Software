# Organ-Donation-Matching-System
A Python + MySQL based organ donation and matching management system.

Organ Donation Matching System (ODMS)

A Python + MySQL based Organ Donation and Matching Management System designed to assist hospitals, donors, and recipients by streamlining organ requests, donor registration, and automated organ-matching logic.

## 📊 System Flowchart

![Flowchart](Flow%20Chart.png)

## 📸 Program Output Screenshots

Below are screenshots of the working Organ Donation Matching System:

![Outputs](Outputs_ODMS_Screenshots.txt)


• Project Overview

The Organ Donation Matching System (ODMS) is a console-based application developed using:

- Python
- MySQL Database
- mysql.connector
- Modular function-based approach
- Dynamic hospital-specific table creation

The system supports:

- Donor registration
- Recipient (patient) registration
- Organ request generation
- Compatibility checking (blood group based)
- Automated organ-matching
- Notifications for matched donors
- Hospital-wise data separation

---

• Key Features

* Donor Module

- Register donors with personal, medical, and organ details
- Store donor info in hospital-specific tables
- Validate blood group, organ type, age, etc.

* Recipient Module

- Register patients requiring an organ
- Raise an organ request
- Connect patient details to organ type

* Organ Matching

- Automated match check based on:
   - Blood group compatibility
   - Organ type
   - Availability
- Sends simulated “notification” when a match is found

* Hospital-wise Database Structure

Each hospital gets:

- A donor table
- A recipient table
- A request table
- A confirmation table

This ensures data separation across hospitals.

---

• Tech Stack

Component| Technology
Backend| Python 3
Database| MySQL
Connector| mysql.connector
Platform| Console-based application

---

• Project Structure

Organ-Donation-Matching-System/
│
├── Organ-Donation.py        # Main Python program
├── ODMS.sql                 # Database + table creation script
└── README.md                # Documentation

---

• How to Run the Project

* Install Requirements

Install MySQL connector:

pip install mysql-connector-python

* Import the SQL Database

Open MySQL and run:

source ODMS.sql;

This will create:

- Database → ODMS
- Global tables → HOSPITALS, REQUESTS, CONFIRMATION

* Configure MySQL Login

Inside "Organ-Donation.py", update:

x = ms.connect(
    host="localhost",
    username="root",
    password="yourpassword",
    database="ODMS"
)

* Run the Program

python Organ-Donation.py

---

• Sample Output (Preview)

----------------------------------------
   ORGAN DONATION MATCHING SYSTEM  
----------------------------------------

1. Donor Registration
2. Recipient Registration
3. Organ Request
4. Match Organ
5. Exit
Enter your choice:

---

📁 Database Summary

Global Tables Created:

- HOSPITALS
- REQUESTS
- CONFIRMATION

Per-Hospital Dynamic Tables:

- donors_<hospital>
- recipients_<hospital>
- requests_<hospital>
- confirmation_<hospital>

---

🎯 Purpose of the Project

This system is ideal for:

- College academic projects
- Real-world hospital workflow simulation
- Internship portfolio projects
- Beginner to intermediate Python + MySQL practice

---

👩‍💻 Developer

Sijenna J
Python & MySQL Developer
Sathyabama University

---

⭐ Show Your Support

If you like this project, give it a star ⭐ on GitHub!
