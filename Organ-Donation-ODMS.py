import os
import time
import random
import platform
import mysql.connector as ms
from datetime import datetime

x=ms.connect(host="localhost",username="root",passwd="root",database="organ_donation_and_requesting_software")

cur=x.cursor()

def create_hospital_table():

        hosp="create table if not exists HOSPITALS(Hospital_ID varchar(100) UNIQUE,H_password varchar(15) PRIMARY KEY,Hospital_Name varchar(50) Not Null,Hospital_Location varchar(100) Not Null,Contact_No decimal(10)) "

        cur.execute(hosp)

        request="create table if not exists REQUESTS(From_hosp_ID varchar(100),To_hosp_ID varchar(100),recipient_ID int,donor_ID int,checked_NOT_checked ENUM('checked','NOT checked') DEFAULT 'NOT checked')"

        cur.execute(request)

        confirm="create table if not exists CONFIRMATION(From_hosp_ID varchar(100),To_hosp_ID varchar(100),Confirm_availability ENUM('Available','Not Available','Reserved') NOT NULL,checked_NOT_checked ENUM('checked','NOT checked') NOT NULL)"

        cur.execute(confirm)

        x.commit()




def VALID_password():
        
    password = input("Please enter the PASSWORD\U0001F512\U0001F511:")

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
            print("password must contain at least one special character(!@#$%^&*_)")
        else:
            return password
            break

        password = input("Please enter a VALID password: ")

def Hospital_Register():
    
    cur=x.cursor()

    cur.execute("select * from Hospitals")

    Hospital_details=cur.fetchall()

    Hospital_Name=input("enter name\U0001F9AA:").lower()

    def unique_ID():

        while True:
            unique_numbers = random.sample(range(1, 100), 3)

            uid="".join(Hospital_Name.split())+"_"

            for i in unique_numbers:
                uid=uid+str(i)

            for ids in Hospital_details:

                if ids[0] != uid:

                    return uid

    Hospital_ID=unique_ID()

    print("YOUR ID : ",Hospital_ID)

    H_Password=VALID_password()

    Hospital_Location=input("Enter the Hospital Location  \U0001F4CD")

    Contact_No=int(input("Enter the Contact number  \U0001F4DE"))

    insert="""insert into HOSPITALS(Hospital_ID,H_Password,Hospital_Name,Hospital_Location,Contact_No) values(%s,%s,%s,%s,%s)"""
    data=(Hospital_ID,H_Password,Hospital_Name,Hospital_Location,Contact_No)

    cur.execute(insert,data)

    x.commit()

    donor_table_name=f"{Hospital_ID}_donors"

    donor=f"""create table if not exists {donor_table_name}(donor_NOTTO_ID int,donor_name varchar(30),donor_gender varchar(1),donor_DOB date,donor_age int,donor_phno decimal(10),donor_Address varchar(100),donor_organ_type varchar(20),donor_organ_size varchar(100),donor_blood_type varchar(10),Availability_Status ENUM('Available','Reserved','NOT Available') NOT NULL )"""

    cur.execute(donor)

    recipient_table_name=f"{Hospital_ID}_recipients"

    recipient=f"""create table if not exists {recipient_table_name}(recipient_NOTTO_ID int,recipient_name varchar(30),recipient_gender varchar(1),recipient_DOB date,recipient_age int,recipient_phno decimal(10),recipient_Address varchar(100),recipient_organ_type varchar(20),recipient_organ_size varchar(100),recipient_blood_type varchar(10))"""

    cur.execute(recipient)
    x.commit()
    print("\t\t\tRegistered succcessfully!!!")
    main_menu()


def calculate_age(dob):
    today = datetime.today()
    dob = datetime.strptime(dob, '%Y-%m-%d')
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def blood_type():
        bloodtype=input("Enter the blood type  \U0001FA78").strip()
        valid_blood_types=["A+","A-","B+","B-","AB+","AB-","O+","O-"]
        if bloodtype in valid_blood_types:
            return bloodtype
        else:
            print("\nINVALID BLOOD TYPE !!!\n please entry valid blood type\n")
            blood_type()
            
def organ_type():
        print("\t\t\t>>>ORGAN TISSUE TYPES<<<")

        print("\t\t\t------------------------------\n")

        print("\t\t1.KIDNEY\t\t2.LIVER\t\t3.HEART  \U00002764\U0000FE0F\n")

        print("\t\t4.BLOOD  \U0001FA78\t5.PANCREAS\t6.EYE TISSUES  \U0001F441\n")

        print("\t\t\t\t7.SKIN  ")
        print(107*"=",'\n')
        choice=int(input("Enter your Choice:"))
        if choice==1:
            return "KIDNEY"
            
        elif choice==2:
            return "LIVER"
            
        elif choice==3:
            print("1. HEART VALVE")
            print("2. HEART")
            choice=int(input("Enter your choice"))
            if choice==1:
                return "HEART VALVE"
                
            elif choice==2:
                return "HEART"
                
            else:
                print("\nINVALID ORGAN TYPE !!!\n please entry valid organ type\n")
                organ_type()
        elif choice==4:
            return "BLOOD"
            
        elif choice==5:
            return "PANCREAS"
           
        elif choice==6:
            print("\t\t\t>>>EYE TISSUE TYPES<<<")

            print("\t\t\t-------------------------\n")
            print("\t\t1. CORNEA\t\t\t2. SCLERA\n")
            choice=int(input("Enter your choice:"))
            if choice==1:
                return "CORNEA"
                
            elif choice==2:
                return "SCLERA"
                
            
            else:
                print("\nINVALID ORGAN TYPE !!!\n please entry valid organ type\n")
                organ_type()
        elif choice==7:
            return "SKIN"
            
        else:
            print("\nINVALID CHOICE!!!\nplease enter valid choice\n")
            organ_type()
            

def donor_add():

        print("\t\t\t>>>>PERSONAL DETAILS<<<<")

        print("\t\t\t------------------------------\n")
        donor_NOTTO_ID=input("Enter DONOR's NOTTO \U0001F194")
        donor_name=input("Enter donor's full name \U0001F58B:")
        donor_gender=input("Enter donor's Gender [M/F]\u2642/\u2640")
        if __name__ == "__main__":
                donor_DOB= input("Enter DONOR's date of birth (YYYY-MM-DD): ")
                try:
                        donor_age = calculate_age(donor_DOB)
                except ValueError:
                        print("INVALID date format. Please use YYYY-MM-DD.")

        donor_phno=int(input("Enter the donor's phone number\U0001F4DE:"))
        donor_Address=input("Enter the Address of the Donor  \U0001F3E0:")
        print(106*"=",'\n')

        print("\t\t\t>>>>MEDICAL INfORMATION<<<<")

        print("\t\t\t----------------------------------\n")
        donor_organ_type=organ_type()
        donor_organ_size=input("Enter the size of the Organ [(Length)cm x (Width)cm x (Thickness)cm]/ Blood units").lower().strip()

        donor_blood_type=blood_type()
        Valid_Availability_Status=['available','reserved','not available']

        Availability_Status=input("Enter the Availability Status ['Available','Reserved','NOT Available'] : ")

        while Availability_Status.lower() not in Valid_Availability_Status:
                print("INVALID Availability Status!!!")

                Availability_Status=input("Enter the Availability Status ['Available','Reserved','NOT Available'] : ")

        cur=x.cursor()
        donor_table_name=f"{ID[0]}_donors"

        insert=f"""insert into {donor_table_name}(donor_NOTTO_ID,donor_name,donor_gender,donor_DOB,donor_age,donor_phno,donor_Address,donor_organ_type,donor_organ_size,donor_blood_type,Availability_Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        data=(donor_NOTTO_ID,donor_name,donor_gender,donor_DOB,donor_age,donor_phno,donor_Address,donor_organ_type,donor_organ_size,donor_blood_type,Availability_Status)

        cur.execute(insert,data)
        x.commit()
        ans=input("Enter y to add more DONORS: ").lower()
        print(106*"=",'\n')
        if ans=="y":
                donor_add()
        else:
                donor_menu()
                
                

def recipient_add():

        print("\t\t\t>>>>PERSONAL DETAILS<<<<")

        print("\t\t\t------------------------------\n")
        recipient_NOTTO_ID=input("Enter RECIPIENT's NOTTO \U0001F194")
        recipient_name=input("Enter recipient's full name \U0001F58B:")
        recipient_gender=input("Enter recipient's gender \u2642/\u2640:")
        if __name__ == "__main__":

                recipient_DOB= input("Enter recipient's date of birth (YYYY-MM-DD): ")
                try:
                        recipient_age = calculate_age(recipient_DOB)
                except ValueError:
                        print("INVALID date format. Please use YYYY-MM-DD.")

        recipient_phno=int(input("Enter the recipient's phone \U0001F4DE"))
        recipient_address=input("Enter the recipient's address \U0001F3E0")
        print(106*"=",'\n')

        print("\t\t\t>>>>MEDICAL INfORMATION<<<<")

        print("\t\t\t----------------------------------\n")
        recipient_organ_type=organ_type()

        recipient_organ_size=input("Enter the size of the Organ[(Length)cm x (Width)cm x (Thickness)cm]/ Blood units").strip()

        recipient_blood_type=blood_type()
        cur=x.cursor()
        recipient_table_name=f"{ID[0]}_recipients"

        insert=f"""insert into {recipient_table_name}(recipient_NOTTO_ID,recipient_name,recipient_gender,recipient_DOB,recipient_age,recipient_phno,recipient_Address,recipient_organ_type,recipient_organ_size,recipient_blood_type) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        data=(recipient_NOTTO_ID,recipient_name,recipient_gender,recipient_DOB,recipient_age,recipient_phno,recipient_Address,recipient_organ_type,recipient_organ_size,recipient_blood_type)

        cur.execute(insert,data)
        x.commit()
        ans=input("Enter y to add more RECIPIENT: ").lower()
        print(106*"=",'\n')
        if ans=="y":
                recipient_add()
        else:
                recipient_menu()


def Update_Donor():

    print("\t\t\t>>>UPDATE DONOR DETAILS<<<")

    print("\t\t\t-----------------------------------\n")
    donor_table_name = f"{ID[0]}_donors"

    donor_NOTTO_ID = int(input("Enter the DONOR's NOTTO \U0001F194:"))

    print("\t1.Donor's Phone number \U0001F4DE\t\t2.Donor's Address   \U0001F3E0")

    print("\t3.Donor's Organ type  \U0001F9E0\t\t4.Donor's Organ size \U0001F52C")

    print("\t5.Donor's Blood type  \U0001FA78\t\t6.Availability Status")
    choice = int(input("Enter the choice you want to UPDATE:"))
    
    if choice == 1:
        donor_phno = int(input("Enter the NEW phone number \U0001F4DE"))
        cur = x.cursor()

        update = f"""UPDATE {donor_table_name} SET donor_phno = %s WHERE donor_NOTTO_ID = %s"""
        cur.execute(update, (donor_phno, donor_NOTTO_ID))
        x.commit()
    
    elif choice == 2:
        donor_Address = input("Enter the NEW address: \U0001F3E0 ")
        cur = x.cursor()

        update = f"""UPDATE {donor_table_name} SET donor_Address = %s WHERE donor_NOTTO_ID = %s"""

        cur.execute(update, (donor_Address, donor_NOTTO_ID))
        x.commit()
    
    elif choice == 3:
        donor_organ_type = organ_type()
        cur = x.cursor()

        update = f"""UPDATE {donor_table_name} SET donor_organ_type = %s WHERE donor_NOTTO_ID = %s"""

        cur.execute(update, (donor_organ_type, donor_NOTTO_ID))
        x.commit()
    
    elif choice == 4:
        donor_organ_size = input("Enter the Organ Size: ")
        cur = x.cursor()

        update = f"""UPDATE {donor_table_name} SET donor_organ_size = %s WHERE donor_NOTTO_ID = %s"""

        cur.execute(update, (donor_organ_size, donor_NOTTO_ID))
        x.commit()
    
    elif choice == 5:
        donor_blood_type = blood_type()
        cur = x.cursor()

        update = f"""UPDATE {donor_table_name} SET donor_blood_type = %s WHERE donor_NOTTO_ID = %s"""

        cur.execute(update, (donor_blood_type, donor_NOTTO_ID))
        x.commit()
    
    elif choice == 6:
        Valid_Availability_Status = ['available', 'reserved', 'not available']

        Availability_Status = input("Enter the Availability Status ['Available','Reserved','NOT Available'] : ")
        
        
        while Availability_Status.lower() not in Valid_Availability_Status:
            print("INVALID Availability Status!!!")

            Availability_Status = input("Enter the Availability Status ['Available','Reserved','NOT Available'] : ")
        
        cur = x.cursor()

        update = f"""UPDATE {donor_table_name} SET Availability_Status = %s WHERE donor_NOTTO_ID = %s"""

        cur.execute(update, (Availability_Status, donor_NOTTO_ID))
        x.commit()
    
    ans = input("Enter y to update more donor details : ").lower()
    print(106*"=",'\n')
    if ans == "y":
        Update_Donor()
    else:
        donor_menu()

                
def Update_Recipient():

        print("\t\t\t>>>UPDATE RECIPIENT DETAILS<<<")

        print("\t\t\t-----------------------------------\n")
        recipient_table_name = f"{ID[0]}_recipients"

        recipient_NOTTO_ID = int(input("Enter recipient's NOTTO ID\U0001F194 : "))
        
        print("\t1.Recipient's Phone number\U0001F4DE:\t 2.Recipient's Address \U0001F3E0:")

        print("\t3.Recipient's Organ type\U0001F9E0 : \t4.Recipient's Organ size\U0001F52C :")

        print("\t5.Recipient's Blood type \U0001FA78 : \t6.EXIT\n")
        
        choice = int(input("Enter the choice you want to UPDATE: "))
        
        if choice == 1:

            recipient_phno = int(input("Enter the NEW phone number\U0001F4DE : "))
            cur = x.cursor()

            update = f"""UPDATE {recipient_table_name} SET recipient_phno = %s WHERE recipient_NOTTO_ID = %s"""

            cur.execute(update, (recipient_phno, recipient_NOTTO_ID))
            x.commit()
        
        elif choice == 2:
            recipient_Address = input("Enter the NEW address\U0001F3E0 : ")
            cur = x.cursor()

            update = f"""UPDATE {recipient_table_name} SET recipient_Address = %s WHERE recipient_NOTTO_ID = %s"""

            cur.execute(update, (recipient_Address, recipient_NOTTO_ID))
            x.commit()
        
        elif choice == 3:
            recipient_organ_type = organ_type()  
            cur = x.cursor()

            update = f"""UPDATE {recipient_table_name} SET recipient_organ_type = %s WHERE recipient_NOTTO_ID = %s"""

            cur.execute(update, (recipient_organ_type, recipient_NOTTO_ID))
            x.commit()
        
        elif choice == 4:
            recipient_organ_size = input("Enter the Organ Size: ").lower()
            cur = x.cursor()

            update = f"""UPDATE {recipient_table_name} SET recipient_organ_size = %s WHERE recipient_NOTTO_ID = %s"""

            cur.execute(update, (recipient_organ_size, recipient_NOTTO_ID))
            x.commit()
        
        elif choice == 5:
            recipient_blood_type = blood_type()  
            cur = x.cursor()

            update = f"""UPDATE {recipient_table_name} SET recipient_blood_type = %s WHERE recipient_NOTTO_ID = %s"""

            cur.execute(update, (recipient_blood_type, recipient_NOTTO_ID))
            x.commit()
       
        ans = input("Enter 'y' to update more recipient details, or any other key to exit: ").lower()

        if ans=="y":
                Update_Recipient()
        else:
                recipient_menu()

def search_donor():

    while True:
            donor_ID = int(input("\nEnter donor's NOTTO ID: "))
            donor_table_name = f"{ID[0]}_donors"
            cur = x.cursor()
            check_donor =  f"SELECT COUNT(*) FROM {donor_table_name} WHERE donor_NOTTO_ID = %s"

            cur.execute(check_donor,(donor_ID,))
            count = cur.fetchone()[0]
            if count == 0:

                    print(f"Donor with NOTTO ID {donor_ID} not found. Please enter a valid NOTTO ID.")

                    continue  
       
            donor_detail = f"SELECT * FROM {donor_table_name} WHERE donor_NOTTO_ID = %s"

            cur.execute(donor_detail, (donor_ID,))
            donor_list = cur.fetchone()

            if donor_list:
                    H_donor = [i[0] for i in cur.description]
                    for i, j in zip(H_donor, donor_list):
                            print(i, " : ", j)

            continue_search = input("\nDo you want to search for another donor? (yes/no): ").lower()

            if continue_search =="yes":
                    search_donor()
            else:
                    donor_menu()
       


def search_recipient():

    while True:
        recipient_ID = int(input("\nEnter recipient's NOTTO ID: "))
        recipient_table_name = f"{ID[0]}_recipients"
        cur = x.cursor()
        check_recipient = f"SELECT COUNT(*) FROM {recipient_table_name} WHERE recipient_NOTTO_ID = %s"

        cur.execute(check_recipient, (recipient_ID,))
        count = cur.fetchone()[0]

        if count == 0:

            print(f"Recipient with NOTTO ID {recipient_ID} not found. Please enter a valid NOTTO ID.")

            continue         

        recipient_detail = f"SELECT * FROM {recipient_table_name} WHERE recipient_NOTTO_ID = %s"

        cur.execute(recipient_detail, (recipient_ID,))
        recipient_list = cur.fetchone()
        if recipient_list:
            H_recipient = [i[0] for i in cur.description]
            for i, j in zip(H_recipient, recipient_list):
                print(i, " : ", j)

        continue_search = input("\nDo you want to search for another recipient? (yes/no): ").lower()

        if continue_search =="yes":
                search_recipient()
        else:
                recipient_menu()

def delete_donor():

    while True:
            donor_ID=int(input("Enter Donor's NOTTO ID"))
            donor_table_name=f"{ID[0]}_donors"
            cur=x.cursor()

            check_donor =  f"SELECT COUNT(*) FROM {donor_table_name} WHERE donor_NOTTO_ID = %s"

            cur.execute(check_donor,(donor_ID,))
            count = cur.fetchone()[0]

            if count == 0:

                    print(f"Donor with NOTTO ID {donor_ID} not found. Please enter a valid NOTTO ID.")

                    continue

            donor_del = f"DELETE FROM  {donor_table_name} WHERE donor_NOTTO_ID = %s"

            cur.execute(donor_del, (donor_ID,))
            x.commit()
            print("Donor deleted successfully !!!")

            continue_del= input("\nDo you want to delete another donor? (yes/no): ").lower()

            if continue_search =="yes":
                    delete_donor()
            else:
                    donor_menu()
       
                    
def delete_recipient():

    while True:
            recipient_ID=int(input("Enter Recipient's NOTTO ID"))
            recipient_table_name=f"{ID[0]}_recipients"
            cur=x.cursor()

            check_recipient =  f"SELECT COUNT(*) FROM {recipient_table_name} WHERE recipient_NOTTO_ID = %s"

            cur.execute(check_recipient,(recipient_ID,))
            count = cur.fetchone()[0]
            if count == 0:
                    print(f"Recipient with NOTTO ID {recipient_ID} not found. Please enter a valid NOTTO ID.")

                    continue

            recipient_del = f"DELETE FROM  {recipient_table_name} WHERE recipient_NOTTO_ID = %s"

            cur.execute(recipient_del, (recipient_ID,))
            x.commit()
            print("Recipient deleted successfully !!!")

            continue_del= input("\nDo you want to delete another recipient? (yes/no): ").lower()

            if continue_search =="yes":
                    delete_recipient()
            else:
                    recipient_menu()

def view_donor_list():

    donor_table_name = f"{ID[0]}_donors"
    cur = x.cursor()
    donor_list = f"select * from {donor_table_name}"
    cur.execute(donor_list)
    data = cur.fetchall()
    H_donor = [i[0] for i in cur.description]
    for i in range(len(data)):
        print(f"DONOR {i+1}:")
        print("-"*192)
        donor_info = dict(zip(H_donor, data[i]))
        for key, value in donor_info.items():
            print(f"{key} : {value}")
        print("\n" + "-"*192)  
    x.commit()
    print("="*106)
    donor_menu()
    


def view_recipient_list():

    recipient_table_name = f"{ID[0]}_recipients"
    cur = x.cursor()
    recipient_list = f"select * from {recipient_table_name}"
    cur.execute(recipient_list)
    data = cur.fetchall()
    H_recipient = [i[0] for i in cur.description]
    for i in range(len(data)):
        print(f"RECIPIENT{i+1}:")
        print("-"*192)
        recipient_info = dict(zip(H_recipient, data[i]))
        for key, value in recipient_info.items():
            print(f"{key} : {value}")
        print("\n" + "-"*192)  
    x.commit()
    print("="*106)
    recipient_menu()
                    

def donor_menu():

    print(192*"-")

    print("\n\t\t\t\tDONOR MENU\n")

    print("\t\t1. Add Donor \U00002795 \U0001F464\t\t2. Update Donor \U00002795\n")

    print("\t\t3. Search Donor \U0001F50E\t\t4. Delete Donor \u274C\n")

    print("\t\t5. View Donor list \U0001F4CB\t6. EXIT \U0001F6B6\n")

    choice=int(input("Enter your choice:"))
    print(192*"-","\n")
    if choice==1:
        donor_add()
    elif choice==2:
        Update_Donor()
    elif choice==3:
        search_donor()
    elif choice==4:
        delete_donor()
    elif choice==5:
        view_donor_list()
    elif choice==6:
        Hospital_menu()
    else:
        print("INVALID Choice!!!\nPlease Enter VALID choice\n")
        donor_menu()
        
def recipient_menu():

    print(192*"-")

    print("\n\t\t\t\tRECIPIENT MENU\n")

    print("\t\t1. Add Recipient \U00002795 \U0001F464\t\t2. Update Recipient \U00002795\n")

    print("\t\t3. Search Recipient \U0001F50E\t\t4. Delete  \u274C\n")

    print("\t\t5. View Recipient list \U0001F4CB\t\t6. EXIT \U0001F6B6\n")

    choice=int(input("Enter your choice:"))
    print(192*"-","\n")
    if choice==1:
        recipient_add()
    elif choice==2:
        Update_Recipient()
    elif choice==3:
        search_recipient()
    elif choice==4:
        delete_recipient()
    elif choice==5:
        view_recipient_list()
    elif choice==6:
        Hospital_menu()
    else:
        print("INVALID Choice!!!\nPlease Enter VALID choice\n")
        recipient_menu()
    

def send_notification(title, message):

    current_platform = platform.system()
    
    if current_platform == "Windows":
        os.system(f'msg * "{message}"')
    elif current_platform == "Darwin":  # macOS

        os.system(f'osascript -e \'display notification "{message}" with title "{title}"\'')

    elif current_platform == "Linux":
        os.system(f'notify-send "{title}" "{message}"')
    else:
        print("Unsupported OS")


def match_organ():

    cur = x.cursor()
    print(106*'=')

    print("\t\t\t\t MATCHING SYSTEM ")

    print(106*'=')
    recipient_ID = int(input("Enter recipient's NOTTO ID to MATCH: "))
    recipient_table_name = f"{ID[0]}_recipients"
   
    recipient_details = f"""SELECT recipient_organ_type, recipient_organ_size 
                            FROM {recipient_table_name} 
                            WHERE recipient_NOTTO_ID = %s"""

    cur.execute(recipient_details, (recipient_ID,))
    data = tuple(cur.fetchall())
    
    if not data:
        print("\t\t\t\tRecipient not found.\u2757")
        print("\t\t\tPlease enter VALID Recipient ID!!!!")
        match_organ()
        return
    
    organ_type, organ_size = data[0]

    print("\t\t\tProccessing Recipient's Details.......\n")

    time.sleep(3)

    print("\t\t\tFinding Match for the Recipient......\n")

    time.sleep(3)
    cur.execute("SHOW TABLES")
    tables = cur.fetchall()
    donor_tables = [table[0] for table in tables if table[0].endswith('_donors')]
    
    matched_donors = []


    for table in donor_tables:

        query = f"""SELECT EXISTS(SELECT * FROM {table} 
                                   WHERE donor_organ_type = %s 
                                   AND donor_organ_size = %s 
                                   AND Availability_Status = 'Available')"""

        cur.execute(query, (organ_type, organ_size))
        organ_match = cur.fetchone()
        
        if organ_match[0] == 1:

            query_donor = f"""SELECT donor_NOTTO_ID, donor_name, donor_gender, donor_DOB, donor_age, donor_phno, donor_Address, donor_organ_type, donor_organ_size, donor_blood_type FROM {table} WHERE donor_organ_type = %s AND donor_organ_size = %s"""

            cur.execute(query_donor, (organ_type, organ_size))
            blood_donor = cur.fetchall()
            
            for donor in blood_donor:
                donor_blood = donor[9]  
                donor_ID = donor[0]
                
                
                query_recipient = f"""SELECT recipient_blood_type 
                                      FROM {recipient_table_name} 
                                      WHERE recipient_NOTTO_ID = %s"""

                cur.execute(query_recipient, (recipient_ID,))
                blood_recipient = cur.fetchall()

                for recipient in blood_recipient:
                    recipient_blood = recipient[0]

           
                    if is_compatible(donor_blood, recipient_blood):
                        matched_donors.append(donor)

                        print("\t\t\t\tMATCH FOUND!!!\n")

                        time.sleep(1)
                        print(f"\t\t\t{donor_ID} can donate organ to {recipient_ID}.")
                    else:
                        print(f"\t\tNo donor match found for {recipient_ID}.")

    if matched_donors:

        print("\nMATCHED DONORS :\n")

        for donor in matched_donors:

            print(
                f"Donor NOTTO ID: {donor[0]}\n"
                f"Donor name: {donor[1]}\n"
                f"Donor gender: {donor[2]}\n"
                f"Donor DOB: {donor[3]}\n"
                f"Donor age: {donor[4]}\n"
                f"Donor phno: {donor[5]}\n"
                f"Donor Address: {donor[6]}\n"
                f"Donor organ type: {donor[7]}\n"
                f"Donor blood type: {donor[9]}\n"
                f"Availability Status: Available\n\n"
                )
     
        donor_matched_ID = int(input("Enter the DONOR's ID to SEND CONFIRMATION REQUEST: "))
        
        for table_name in donor_tables:

            query = f"SELECT  donor_name  FROM {table_name} WHERE donor_NOTTO_ID = %s"

            cur.execute(query, (donor_matched_ID,))
            result = cur.fetchone()
        
            if result:
                
                hospital_ID= table_name.replace("_donors", "")
                
                send_request = """INSERT INTO requests(From_hosp_ID, To_hosp_ID, recipient_ID, donor_ID, checked_NOT_checked) 
                                  VALUES(%s, %s, %s, %s, %s)"""

                values = (ID[0], hospital_ID, recipient_ID, donor_matched_ID, 'NOT checked')

                cur.execute(send_request, values)
                x.commit()

                print("\n\t\tConfirmation request sent successfully!!!\n")

                ask=input("Do you want to match any other recipient (Yes/No): ").strip()
                if ask=="yes":
                    match_organ()
                else:
                    Hospital_menu()
                return

    else:
        print("NO matched donors found.")
        ask=input("Do you want to match any other recipient (Yes/No): ").strip()
        if ask=="yes":
            match_organ()
        else:
            Hospital_menu()
    print(106*'=')

def is_compatible(donor: str, recipient: str) -> bool:

    blood_compatibility = {
        'O-': ['O-', 'A-', 'B-', 'AB-', 'O+', 'A+', 'B+', 'AB+'],
        'O+': ['O+', 'A+', 'B+', 'AB+'],
        'A-': ['A-', 'AB-', 'A+', 'AB+'],
        'A+': ['A+', 'AB+'],
        'B-': ['B-', 'AB-', 'B+', 'AB+'],
        'B+': ['B+', 'AB+'],
        'AB-': ['AB-', 'AB+'],
        'AB+': ['AB+']
    }
    
    donor = donor.upper()
    recipient = recipient.upper()
    
    if donor in blood_compatibility:
        return recipient in blood_compatibility[donor]
    else:
        raise ValueError("Invalid blood type input.")

def Hospital_menu():

    print(192*"-")

    print("\n\t\t\t\tMAIN MENU\n")

    print("\t\t1. Donors\t\t\t\t2. Recipients\n")
    print("\t\t3. Match Organ\t\t\t4. EXIT\n")
    choice=int(input("Enter your choice:"))
    print(192*"-","\n")
    if choice==1:
            donor_menu()
    elif choice==2:
            recipient_menu()
    elif choice==3:
            match_organ()
    elif choice==4:
            main_menu()
    else:
            print("Enter a VALID choice!!!!\n")
            Hospital_menu()

def confirmation():

    cur = x.cursor()

    query = "SELECT * FROM confirmation WHERE checked_NOT_checked='NOT checked'"

    cur.execute(query)
    confirm_requests = cur.fetchall()

    has_pending_requests = False  

    for confirm_request in confirm_requests:
        if confirm_request[1] == ID[0]:
            has_pending_requests = True  

            send_notification("Hello!", "Got a Confirmation Notification!!!")
            y_n = input("Do you want to open the confirmation request NOW!!! (Yes/No) : ").lower()
            
            if y_n == "yes":
                
                hospital_name = confirm_request[0].split('_')[0]

                query = "SELECT Hospital_Name, Hospital_Location, Contact_No FROM hospitals WHERE Hospital_ID=%s"

                cur.execute(query,(confirm_request[0],))
                hosp_details=cur.fetchall()
                print("Hospital Name : ",hosp_details[0][0])
                print("Hospital Location : ",hosp_details[0][1])
                print("Contact No : ",hosp_details[0][2])
                print("Recipient ID : ",confirm_request[4])
                print("Matched Donor ID : ",confirm_request[5])

                upt_query = "UPDATE confirmation SET checked_NOT_checked='checked' WHERE recipient_ID=%s AND donor_ID=%s"

                upt_info = (confirm_request[4], confirm_request[5])
                cur.execute(upt_query, upt_info)
                x.commit()

    return has_pending_requests 
 
def request():

    cur = x.cursor()

    query = "SELECT * FROM requests WHERE checked_NOT_checked = 'NOT checked'"

    cur.execute(query)
    requests = cur.fetchall()  
    
    if len(requests) > 0:
        print("Requests fetched successfully")
    
    for request in requests:
        if request[1] == ID[0]:
            hospital_name = request[0].split("_")
            Rhospital_name = request[0] + "_recipients"
            Dhospital_name = ID[0] + "_donors"
            message = "Got an organ request from: " + hospital_name[0]
            send_notification("Hello!", message)
            print(f"From_hospital: {Rhospital_name}\n")
            print("\tRecipient Details:\n")
            
            query = f"SELECT * FROM {Rhospital_name} WHERE recipient_NOTTO_ID = %s"

            cur.execute(query, (request[2],))
            recipient_detail = cur.fetchone()
            
            print("\n\t\t# Recipient Details📄:\n")
            
            print("\n\t\t\t Recipient NOTTO ID :",recipient_detail[0])
            print("\t\t\t Recipient Name :",recipient_detail[1])
            print("\t\t\t Recipient Gender :",recipient_detail[2])
            print("\t\t\t Recipient DOB :",recipient_detail[3])
            print("\t\t\t Recipient Age :",recipient_detail[4])
            print("\t\t\t Recipient Phno:",recipient_detail[5])
            print("\t\t\t Recipient Address :",recipient_detail[6])
            print("\t\t\t Recipient Organ type :",recipient_detail[7])
            print("\t\t\t Recipient Organ size/blood units :",recipient_detail[8])
            print("\t\t\t Recipient Blood type :",recipient_detail[9])
                
            print("\t\nMatched Donor Details:\n")
            
            query = f"SELECT * FROM {Dhospital_name} WHERE donor_NOTTO_ID = %s"

            cur.execute(query, (request[3],))
            donor_detail = cur.fetchone()
            
            print("\n\t\t# Donor Details📄:\n")
            
            print("\n\t\t\t Donor NOTTO ID :",donor_detail[0])
            print("\t\t\t Donor Name :",donor_detail[1])
            print("\t\t\t Donor Gender :",donor_detail[2])
            print("\t\t\t Donor DOB :",donor_detail[3])
            print("\t\t\t Donor Age :",donor_detail[4])
            print("\t\t\t Donor Phno:",donor_detail[5])
            print("\t\t\t Donor Address :",donor_detail[6])
            print("\t\t\t Donor Organ type :",donor_detail[7])
            print("\t\t\t Donor Organ size/blood units :",donor_detail[8])
            print("\t\t\t Donor Blood type :",donor_detail[9])

            print("\t\t\t Donor Availability Status ['Available'/'Not Available'/'Reserved']:",donor_detail[10])

            print("\n\t\t\tWhether the DONOR is available???")
            print("Enter ['Available'/'Not Available'/'Reserved']")
            Confirm_availability = input()
            
            insert_query = "INSERT INTO confirmation (From_hosp_ID, To_hosp_ID, Confirm_availability, checked_NOT_checked, recipient_ID, donor_ID) VALUES (%s, %s, %s, %s, %s, %s)"        
   
            info = (ID[0], request[0], Confirm_availability, 'NOT checked', request[2], request[3])

            cur.execute(insert_query, info)
            
            upt_query = """UPDATE requests SET checked_NOT_checked = 'checked' WHERE recipient_ID = %s AND donor_ID = %s"""

            upt_info = (request[2], request[3])
            cur.execute(upt_query, upt_info)
            
            x.commit()  
            return True  
            
        else:
            return True


def admin_menu():
    
    print("\t\t\tAdmin Menu\U0001F6E1\U0001F4CB:\n")

    print("\t1. View Pending Requests\t\t2. View Pending Confirmations")
    print("\t3. View Hospital Details\t\t4. Exit\U0001F6B6\n")
    choice = int(input("Enter your choice\U0001F4DD: "))
    
    if choice == 1:
        view_pending_requests()
    elif choice == 2:
        view_pending_confirmations()
    elif choice == 3:
        view_hospital_details()
    elif choice == 4:
        print("Exiting Admin Menu...\U0001F6AA\U0001F6B6")
        main_menu() 
    else:
        print("Invalid choice, please try again.")
        admin_menu()

def view_pending_requests():
    cur = x.cursor()
    query = "SELECT * FROM requests WHERE checked_NOT_checked = 'NOT checked'"
    cur.execute(query)
    requests = cur.fetchall()
    
    if not requests:
        print("No pending requests found.")
    else:
        print("Pending Requests:")
        for request in requests:
            print(f"From Hospital: {request[0]}, To Hospital: {request[1]}")
            print(f"Recipient ID: {request[2]}, Donor ID: {request[3]}")
    
    admin_menu()

def view_pending_confirmations():

    cur = x.cursor()

    query = "SELECT * FROM confirmation WHERE checked_NOT_checked = 'NOT checked'"

    cur.execute(query)
    confirmations = cur.fetchall()
    
    if not confirmations:
        print("No pending confirmations found.")
    else:
        print("Pending Confirmations:")
        for confirmation in confirmations:

            print(f"From Hospital: {confirmation[0]}, To Hospital: {confirmation[1]}")

            print(f"Recipient ID: {confirmation[4]}, Donor ID: {confirmation[5]}")
    
    admin_menu()

def view_hospital_details():

    cur = x.cursor()
    query = "SELECT * FROM hospitals"
    cur.execute(query)
    hospitals = cur.fetchall()
    
    if not hospitals:
        print("No hospital details found.")
    else:
        print("Hospital Details:")
        for hospital in hospitals:
            print(192*"-")
            print("HOSPITAL : ", hospitals.index(hospital)+1)
            print(192*"-")
            print(f"Hospital ID\U0001F3E5: {hospital[0]}")
            print(f"Hospital PASSWORD\U0001F512\U0001F511: {hospital[1]}")
            print(f"Hospital NAME\U0001F489\U0001F3E5: {hospital[2]}")

            print(f"Hospital LOCATION\U0001F3EA\U0001F4CD : {hospital[3]}")

            print(f"Contact NO\U0001F4DE: {hospital[4]}")
            print(106*"=")
    
    admin_menu()


def admin_login():

    admin_id = input("Enter Admin ID\U0001F6E1: ").strip()

    admin_password = input("Please enter the PASSWORD\U0001F512\U0001F511:")

    if admin_id == "admin7" and admin_password == "miskrit":
        print(192*"-")

        print("\t\t\tADMIN LOGIN SUCCESSFUL !!!\U00002705\U0001F511...")

        print(192*"-","\n")
        admin_menu()
    else:
        print("Invalid Admin credentials.")
        main_menu()



ID=["NONE"]

def main_menu():

    print(106*"~")
    print(106*"~")

    print("\t\t\t\t ORGAN  DONATION\n")
    print("\t\t\t\t      AND\n")
    print("\t\t\t\tMATCHING SOFTWARE")

    print(106*"~")
    print(106*"~",'\n')

    print("\t\t1. ADMIN\U0001F6E1\t2. USER LOGIN\U0001F5A5\t  3. USER REGISTER\U0001F4DD\n")

    choice=int(input("Enter your choice : "))

    def message():

         print(192*"-")

         print("\t\t\tWelcome to the Organ Donation & Matching System!\n")

         print("\t\t\t\tInitializing system.......\n")
         print(137*'*')

         print( "\t\t\tOne ORGAN donor can SAVE 8 lives.Be a HERO; be a donor.")

         print(137*'*')
         time.sleep(3)

         print("\t\t\t\t\tSystem Ready!")

         print(192*"-","\n")
    message()

    if choice==1:
        create_hospital_table()
        admin_login()
    elif choice==2:
        ans="y"
        while ans=="y":
            cur=x.cursor()
            cur.execute("select * from Hospitals")
            Hospital_details=cur.fetchall()

            UID=input("Enter the Hospital/Transplant Centre ID\U0001F489:").strip()

            passwd=input("Enter the password\U0001F512\U0001F511:").strip()
            for i in Hospital_details:
                if i[0]==UID and i[1]==passwd:
                    ID[0]=UID
                    if confirmation():
                        pass
                    if request():
                        pass
                    Hospital_menu()
                    break             
                    
            print("INVALID ID or Password!!!!\nPlease Enter VALID ID or Password")

    elif choice==3:
        Hospital_Register()
    else:
        print("Enter a VALID choice!!!!\n")
        main_menu()
        
        
main_menu()
