import os
import time
import random
import platform
import mysql.connector as ms
from datetime import datetime

# ========== DATABASE CONNECTION ==========
# Adjust password if needed
try:
    x = ms.connect(
        host="localhost",
        user="root",
        password="root",
        database="organ_donation_and_requesting_software",
        auth_plugin="mysql_native_password"
    )
except Exception as e:
    print("\n❌ ERROR connecting to MySQL:", e)
    print("Make sure MySQL server is ON and credentials are correct.")
    exit()

cur = x.cursor()

# ========== CREATE GLOBAL TABLES ==========
def create_hospital_table():
    hosp = """CREATE TABLE IF NOT EXISTS hospitals(
        Hospital_ID VARCHAR(100) NOT NULL PRIMARY KEY,
        H_password VARCHAR(255) NOT NULL,
        Hospital_Name VARCHAR(100) NOT NULL,
        Hospital_Location VARCHAR(255) NOT NULL,
        Contact_No VARCHAR(20)
    )"""
    cur.execute(hosp)

    request = """CREATE TABLE IF NOT EXISTS requests(
        From_hosp_ID VARCHAR(100),
        To_hosp_ID VARCHAR(100),
        recipient_ID INT,
        donor_ID INT,
        checked_NOT_checked ENUM('checked','NOT checked') DEFAULT 'NOT checked'
    )"""
    cur.execute(request)

    confirm = """CREATE TABLE IF NOT EXISTS confirmation(
        From_hosp_ID VARCHAR(100),
        To_hosp_ID VARCHAR(100),
        Confirm_availability ENUM('Available','Not Available','Reserved') NOT NULL,
        checked_NOT_checked ENUM('checked','NOT checked') NOT NULL,
        recipient_ID INT,
        donor_ID INT
    )"""
    cur.execute(confirm)

    x.commit()

# ========== PASSWORD VALIDATION ==========
def VALID_password():
    password = input("Please enter the PASSWORD 🔒:")

    while True:
        if len(password) < 8:
            print("Password must be at least 8 characters long.")
        elif not any(char.isupper() for char in password):
            print("Password must contain at least one uppercase letter.")
        elif not any(char.islower() for char in password):
            print("Password must contain at least one lowercase letter.")
        elif not any(char.isdigit() for char in password):
            print("Password must contain at least one number.")
        elif not any(char in "!@#$%^~&*_" for char in password):
            print("Password must contain at least one special character (!@#$%^&*_)")
        else:
            return password

        password = input("Please enter a VALID password: ")

# ========== HOSPITAL REGISTER ==========
def Hospital_Register():
    cur.execute("SELECT Hospital_ID FROM hospitals")
    existing_ids = [row[0] for row in cur.fetchall()]

    Hospital_Name = input("Enter Hospital Name 🏥: ").strip().lower()

    def unique_ID():
        base = "".join(Hospital_Name.split())
        while True:
            nums = random.sample(range(1, 100), 3)
            uid = base + "_" + "".join(str(n) for n in nums)
            if uid not in existing_ids:
                return uid

    Hospital_ID = unique_ID()
    print("\nYOUR GENERATED ID:", Hospital_ID)

    H_Password = VALID_password()
    Hospital_Location = input("Enter Hospital Location 📍: ").strip()
    Contact_No = input("Enter Contact Number 📞: ").strip()

    insert = """INSERT INTO hospitals(Hospital_ID,H_password,Hospital_Name,Hospital_Location,Contact_No)
                VALUES(%s,%s,%s,%s,%s)"""
    cur.execute(insert, (Hospital_ID, H_Password, Hospital_Name, Hospital_Location, Contact_No))
    x.commit()

    donor_table = f"{Hospital_ID}_donors"
    recipient_table = f"{Hospital_ID}_recipients"

    donor = f"""CREATE TABLE IF NOT EXISTS `{donor_table}`(
        donor_NOTTO_ID INT,
        donor_name VARCHAR(100),
        donor_gender VARCHAR(1),
        donor_DOB DATE,
        donor_age INT,
        donor_phno VARCHAR(20),
        donor_Address VARCHAR(255),
        donor_organ_type VARCHAR(50),
        donor_organ_size VARCHAR(100),
        donor_blood_type VARCHAR(10),
        Availability_Status ENUM('Available','Reserved','NOT Available') NOT NULL
    )"""
    cur.execute(donor)

    recipient = f"""CREATE TABLE IF NOT EXISTS `{recipient_table}`(
        recipient_NOTTO_ID INT,
        recipient_name VARCHAR(100),
        recipient_gender VARCHAR(1),
        recipient_DOB DATE,
        recipient_age INT,
        recipient_phno VARCHAR(20),
        recipient_Address VARCHAR(255),
        recipient_organ_type VARCHAR(50),
        recipient_organ_size VARCHAR(100),
        recipient_blood_type VARCHAR(10)
    )"""
    cur.execute(recipient)

    x.commit()
    print("\n✔ Registered Successfully!\n")
    main_menu()

# ========== AGE CALCULATOR ==========
def calculate_age(dob):
    today = datetime.today()
    dob = datetime.strptime(dob, "%Y-%m-%d")
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

# ========== BLOOD TYPE ==========
def blood_type():
    blood = input("Enter Blood Type 🩸: ").upper()
    valid = ["A+","A-","B+","B-","AB+","AB-","O+","O-"]
    if blood in valid:
        return blood
    print("INVALID blood type! Try again.")
    return blood_type()

# ========== ORGAN TYPE ==========
def organ_type():
    print("\n1.KIDNEY  2.LIVER  3.HEART ❤️  4.BLOOD 🩸  5.PANCREAS  6.EYE  7.SKIN")
    choice = input("Enter choice: ")

    types = {
        "1":"KIDNEY",
        "2":"LIVER",
        "3":"HEART",
        "4":"BLOOD",
        "5":"PANCREAS",
        "6":"CORNEA",
        "7":"SKIN"
    }
    return types.get(choice, organ_type())

# ============================================
#            DONOR / RECIPIENT FUNCTIONS
# ============================================

ID = ["NONE"]

# ========== ADD DONOR ==========
def donor_add():
    donor_table = f"{ID[0]}_donors"
    donor_ID = int(input("Enter Donor NOTTO ID: "))
    name = input("Name: ")
    gender = input("Gender (M/F): ").upper()
    DOB = input("DOB (YYYY-MM-DD): ")
    age = calculate_age(DOB)
    ph = input("Phone: ")
    address = input("Address: ")
    organ = organ_type()
    size = input("Organ size/blood units: ")
    blood = blood_type()

    q = f"""INSERT INTO {donor_table}
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'Available')"""
    cur.execute(q, (donor_ID,name,gender,DOB,age,ph,address,organ,size,blood))
    x.commit()
    print("✔ Donor added!\n")
    donor_menu()

# ========== ADD RECIPIENT ==========
def recipient_add():
    table = f"{ID[0]}_recipients"
    rID = int(input("Enter Recipient NOTTO ID: "))
    name = input("Name: ")
    gender = input("Gender (M/F): ").upper()
    DOB = input("DOB (YYYY-MM-DD): ")
    age = calculate_age(DOB)
    ph = input("Phone: ")
    address = input("Address: ")
    organ = organ_type()
    size = input("Organ size/blood units: ")
    blood = blood_type()

    q = f"""INSERT INTO {table}
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cur.execute(q, (rID,name,gender,DOB,age,ph,address,organ,size,blood))
    x.commit()
    print("✔ Recipient added!\n")
    recipient_menu()

# ========== UPDATE DONOR ==========
def Update_Donor():
    table = f"{ID[0]}_donors"
    dID = int(input("Enter Donor NOTTO ID to update: "))
    field = input("Which field to update (name,gender,age,etc)? ").lower()
    value = input("Enter new value: ")

    q = f"UPDATE {table} SET {field}=%s WHERE donor_NOTTO_ID=%s"
    cur.execute(q, (value, dID))
    x.commit()
    print("✔ Donor updated!\n")
    donor_menu()

# ========== UPDATE RECIPIENT ==========
def Update_Recipient():
    table = f"{ID[0]}_recipients"
    rID = int(input("Enter Recipient NOTTO ID: "))
    field = input("Which field to update (name,gender,age,etc)? ").lower()
    value = input("Enter new value: ")

    q = f"UPDATE {table} SET {field}=%s WHERE recipient_NOTTO_ID=%s"
    cur.execute(q, (value, rID))
    x.commit()
    print("✔ Recipient updated!\n")
    recipient_menu()

# ========== SEARCH DONOR ==========
def search_donor():
    table = f"{ID[0]}_donors"
    dID = int(input("Enter Donor NOTTO ID: "))

    q = f"SELECT * FROM {table} WHERE donor_NOTTO_ID=%s"
    cur.execute(q, (dID,))
    result = cur.fetchone()

    if result:
        print("\n--- DONOR DETAILS ---")
        cols = [col[0] for col in cur.description]
        for c,v in zip(cols,result):
            print(c,":",v)
    else:
        print("❌ Donor not found.")

    donor_menu()

# ========== SEARCH RECIPIENT ==========
def search_recipient():
    table = f"{ID[0]}_recipients"
    rID = int(input("Enter Recipient NOTTO ID: "))

    q = f"SELECT * FROM {table} WHERE recipient_NOTTO_ID=%s"
    cur.execute(q, (rID,))
    result = cur.fetchone()

    if result:
        print("\n--- RECIPIENT DETAILS ---")
        cols = [col[0] for col in cur.description]
        for c,v in zip(cols,result):
            print(c,":",v)
    else:
        print("❌ Recipient not found.")

    recipient_menu()

# ========== DELETE DONOR ==========
def delete_donor():
    table = f"{ID[0]}_donors"
    dID = int(input("Enter Donor NOTTO ID to delete: "))
    q = f"DELETE FROM {table} WHERE donor_NOTTO_ID=%s"
    cur.execute(q, (dID,))
    x.commit()
    print("✔ Donor deleted!\n")
    donor_menu()

# ========== DELETE RECIPIENT ==========
def delete_recipient():
    table = f"{ID[0]}_recipients"
    rID = int(input("Enter Recipient NOTTO ID: "))
    q = f"DELETE FROM {table} WHERE recipient_NOTTO_ID=%s"
    cur.execute(q, (rID,))
    x.commit()
    print("✔ Recipient deleted!\n")
    recipient_menu()

# ========== VIEW DONOR LIST ==========
def view_donor_list():
    table = f"{ID[0]}_donors"
    q = f"SELECT * FROM {table}"
    cur.execute(q)
    data = cur.fetchall()

    print("\n========= DONOR LIST =========\n")
    for row in data:
        print(row)
    donor_menu()

# ========== VIEW RECIPIENT LIST ==========
def view_recipient_list():
    table = f"{ID[0]}_recipients"
    q = f"SELECT * FROM {table}"
    cur.execute(q)
    data = cur.fetchall()

    print("\n========= RECIPIENT LIST =========\n")
    for row in data:
        print(row)
    recipient_menu()

# ========== BRAIN: BLOOD MATCH ==========
def is_compatible(donor, recipient):
    comp = {
        'O-':['O-','A-','B-','AB-','O+','A+','B+','AB+'],
        'O+':['O+','A+','B+','AB+'],
        'A-':['A-','AB-','A+','AB+'],
        'A+':['A+','AB+'],
        'B-':['B-','AB-','B+','AB+'],
        'B+':['B+','AB+'],
        'AB-':['AB-','AB+'],
        'AB+':['AB+']
    }
    return recipient.upper() in comp.get(donor.upper(), [])

# ========== MATCH ORGANS ==========
def match_organ():
    rtable = f"{ID[0]}_recipients"
    rID = int(input("Enter Recipient NOTTO ID to match: "))

    q = f"SELECT recipient_organ_type, recipient_organ_size FROM {rtable} WHERE recipient_NOTTO_ID=%s"
    cur.execute(q, (rID,))
    res = cur.fetchone()

    if not res:
        print("❌ Recipient not found.")
        Hospital_menu()
        return

    organ, size = res
    print("\nProcessing match...")

    cur.execute("SHOW TABLES")
    tables = cur.fetchall()

    donor_tables = [t[0] for t in tables if t[0].endswith("_donors")]

    matches = []

    for table in donor_tables:
        q = f"""SELECT donor_NOTTO_ID, donor_name, donor_gender, donor_DOB, donor_age, 
                donor_phno, donor_Address, donor_organ_type, donor_organ_size, donor_blood_type 
                FROM {table}
                WHERE donor_organ_type=%s AND donor_organ_size=%s AND Availability_Status='Available'"""
        cur.execute(q, (organ, size))
        donors = cur.fetchall()

        for d in donors:
            donor_blood = d[9]

            q2 = f"SELECT recipient_blood_type FROM {rtable} WHERE recipient_NOTTO_ID=%s"
            cur.execute(q2, (rID,))
            r_blood = cur.fetchone()[0]

            if is_compatible(donor_blood, r_blood):
                matches.append(d)

    if not matches:
        print("\n❌ NO MATCH FOUND.")
        Hospital_menu()
        return

    print("\n✔ MATCHED DONORS:\n")
    for d in matches:
        print(d)

    D = int(input("Enter DONOR ID to send request: "))

    for table in donor_tables:
        q = f"SELECT donor_name FROM {table} WHERE donor_NOTTO_ID=%s"
        cur.execute(q, (D,))
        result = cur.fetchone()

        if result:
            to_hosp = table.replace("_donors", "")
            insert = """INSERT INTO requests VALUES(%s,%s,%s,%s,'NOT checked')"""
            cur.execute(insert, (ID[0], to_hosp, rID, D))
            x.commit()
            print("✔ Request sent!\n")
            Hospital_menu()
            return

# ========== DONOR MENU ==========
def donor_menu():
    print("\n===== DONOR MENU =====")
    print("1. Add Donor")
    print("2. Update Donor")
    print("3. Search Donor")
    print("4. Delete Donor")
    print("5. View Donor List")
    print("6. EXIT")
    ch = input("Enter choice: ")

    if ch=="1": donor_add()
    elif ch=="2": Update_Donor()
    elif ch=="3": search_donor()
    elif ch=="4": delete_donor()
    elif ch=="5": view_donor_list()
    else: Hospital_menu()

# ========== RECIPIENT MENU ==========
def recipient_menu():
    print("\n===== RECIPIENT MENU =====")
    print("1. Add Recipient")
    print("2. Update Recipient")
    print("3. Search Recipient")
    print("4. Delete Recipient")
    print("5. View Recipient List")
    print("6. EXIT")
    ch = input("Enter choice: ")

    if ch=="1": recipient_add()
    elif ch=="2": Update_Recipient()
    elif ch=="3": search_recipient()
    elif ch=="4": delete_recipient()
    elif ch=="5": view_recipient_list()
    else: Hospital_menu()

# ========== CONFIRMATION / REQUEST HANDLERS ==========
def confirmation():
    q = "SELECT * FROM confirmation WHERE checked_NOT_checked='NOT checked'"
    cur.execute(q)
    requests = cur.fetchall()

    for r in requests:
        if r[1] == ID[0]:
            send_notification("Confirmation", "You have a confirmation request")
            print("\n--- CONFIRMATION REQUEST ---")
            print(r)
            q2 = "UPDATE confirmation SET checked_NOT_checked='checked' WHERE recipient_ID=%s AND donor_ID=%s"
            cur.execute(q2, (r[4], r[5]))
            x.commit()
            return True
    return False

def request():
    q = "SELECT * FROM requests WHERE checked_NOT_checked='NOT checked'"
    cur.execute(q)
    reqs = cur.fetchall()

    for r in reqs:
        if r[1] == ID[0]:
            print("\n--- REQUEST RECEIVED ---")
            print("From Hospital:", r[0])
            print("Recipient ID:", r[2])
            print("Donor ID:", r[3])

            Confirm = input("Is donor available? (Available/Not Available/Reserved): ")

            insert = """INSERT INTO confirmation VALUES(%s,%s,%s,'NOT checked',%s,%s)"""
            cur.execute(insert, (ID[0], r[0], Confirm, r[2], r[3]))

            up = "UPDATE requests SET checked_NOT_checked='checked' WHERE recipient_ID=%s AND donor_ID=%s"
            cur.execute(up, (r[2], r[3]))

            x.commit()
            return True

    return False

# ========== ADMIN ==========
def admin_login():
    aid = input("Enter Admin ID: ")
    apass = input("Enter Admin Password: ")

    if aid=="admin7" and apass=="miskrit":
        print("✔ ADMIN LOGIN SUCCESS")
        admin_menu()
    else:
        print("❌ INVALID ADMIN")
        main_menu()

def admin_menu():
    print("\n===== ADMIN MENU =====")
    print("1. View Pending Requests")
    print("2. View Pending Confirmations")
    print("3. View Hospital Details")
    print("4. EXIT")

    ch = input("Enter choice: ")
    if ch=="1": view_pending_requests()
    elif ch=="2": view_pending_confirmations()
    elif ch=="3": view_hospital_details()
    else: main_menu()

def view_pending_requests():
    q = "SELECT * FROM requests WHERE checked_NOT_checked='NOT checked'"
    cur.execute(q)
    reqs = cur.fetchall()
    print("\n--- PENDING REQUESTS ---")
    for r in reqs:
        print(r)
    admin_menu()

def view_pending_confirmations():
    q = "SELECT * FROM confirmation WHERE checked_NOT_checked='NOT checked'"
    cur.execute(q)
    conf = cur.fetchall()
    print("\n--- PENDING CONFIRMATIONS ---")
    for c in conf:
        print(c)
    admin_menu()

def view_hospital_details():
    cur.execute("SELECT * FROM hospitals")
    data = cur.fetchall()

    print("\n===== HOSPITAL DETAILS =====")
    for h in data:
        print(h)
    admin_menu()

# ========== NOTIFICATION (PC) ==========
def send_notification(title, message):
    system = platform.system()
    if system == "Windows":
        os.system(f'msg * "{message}"')
    elif system == "Darwin":
        os.system(f'osascript -e \'display notification "{message}" with title "{title}"\'')
    elif system == "Linux":
        os.system(f'notify-send "{title}" "{message}"')

# ========== MAIN MENU ==========
def main_menu():
    print("\n======= ORGAN DONATION & MATCHING SOFTWARE =======")
    print("1. ADMIN")
    print("2. USER LOGIN")
    print("3. USER REGISTER")
    ch = input("Enter choice: ")

    if ch=="1":
        create_hospital_table()
        admin_login()
    elif ch=="2":
        user_login()
    elif ch=="3":
        Hospital_Register()
    else:
        main_menu()

def user_login():
    cur.execute("SELECT * FROM hospitals")
    hosp = cur.fetchall()

    uid = input("Enter Hospital ID: ").strip()
    pwd = input("Enter Password: ").strip()

    for h in hosp:
        if h[0]==uid and h[1]==pwd:
            ID[0] = uid
            confirmation()
            request()
            Hospital_menu()
            return

    print("❌ INVALID LOGIN")
    user_login()

# ========== HOSPITAL MENU ==========
def Hospital_menu():
    print("\n===== MAIN MENU =====")
    print("1. DONORS")
    print("2. RECIPIENTS")
    print("3. MATCH ORGAN")
    print("4. EXIT")
    ch = input("Enter choice: ")

    if ch=="1": donor_menu()
    elif ch=="2": recipient_menu()
    elif ch=="3": match_organ()
    else: main_menu()

# ========== START PROGRAM ==========
main_menu()