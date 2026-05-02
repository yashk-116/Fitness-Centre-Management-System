import mysql.connector
from datetime import datetime


# MySQL Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="Admin",          
        password="Admin1412", 
        database="fitness_centre_db" 
    )


# Table Structure
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id VARCHAR(20) PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            gender CHAR(1),
            membership_type VARCHAR(20),
            join_date DATE
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Adding Member Function
def add_member():
    print("\n*** Add New Member ***")
    member_id = input("Enter Member ID: ")
    name = input("Enter Name: ")
    age = input("Enter Age: ")
    gender = input("Enter Gender (M/F): ")
    membership_type = input("Enter Membership Type (Gold/Silver/Bronze): ")
    join_date = input("Enter Joining Date (YYYY-MM-DD): ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO members (member_id, name, age, gender, membership_type, join_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (member_id, name, int(age), gender, membership_type, join_date))
    conn.commit()
    cursor.close()
    conn.close()
    print("New Member Added Successfully!")

# Search Member by Name
def search_member_by_name():
    print("\n*** Search Member by Name ***")
    search_name = input("Enter Member Name to Search: ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE name LIKE %s", (f"%{search_name}%",))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if rows:
        for row in rows:
            print("Member Found:", row)
    else:
        print("No Member Found with Related Name.")

# Updating Member
def update_member():
    print("\n*** Update Member Details ***")
    member_id = input("Enter Member ID to Update: ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE member_id = %s", (member_id,))
    row = cursor.fetchone()

    if not row:
        print("No Member Found with the Given ID.")
        cursor.close()
        conn.close()
        return

    print("Current Details:", row)
    new_name = input("Enter New Name (leave blank to keep current): ") or row[1]
    new_age = input("Enter New Age (leave blank to keep current): ") or row[2]
    new_membership = input("Enter New Membership Type (leave blank to keep current): ") or row[4]

    cursor.execute("""
        UPDATE members SET name=%s, age=%s, membership_type=%s
        WHERE member_id=%s
    """, (new_name, int(new_age), new_membership, member_id))
    conn.commit()
    cursor.close()
    conn.close()
    print("..Member Details Updated..")

# Deleting Member
def delete_member():
    print("\n*** Delete Member ***")
    member_id = input("Enter Member ID to Delete: ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM members WHERE member_id = %s", (member_id,))
    affected = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()

    if affected > 0:
        print("..Member Deleted Successfully..")
    else:
        print("No Member Found with the Given ID.")

# Password Verification feature with retrying
def check_password():
    print("---Welcome to Fitness Centre Management System---")
    while True:
        password = input("Enter your Password to access system: ")
        if password == "1414":
            print("Access Granted!")
            break  # Exiting loop and proceeding to menu
        else:
            print("Invalid Password!!!Please Try Again")

# View All Members function
def view_members():
    print("\n*** List of Members ***")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    for row in rows:
        print(row)

# Total Members count
def total_members():
    print("\n*** Total Members ***")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM members")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    print(f"Total Members: {total}")

# Membership Type Counting
def membership_type_count():
    print("\n*** Membership Type Count ***")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT membership_type, COUNT(*) FROM members
        GROUP BY membership_type
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    counts = {"Gold": 0, "Silver": 0, "Bronze": 0}
    for row in rows:
        if row[0] in counts:
            counts[row[0]] = row[1]
    print(f"Gold Members: {counts['Gold']}")
    print(f"Silver Members: {counts['Silver']}")
    print(f"Bronze Members: {counts['Bronze']}")

# Menu to Choose options/Features
def menu():
    while True:
        print("\n --- Welcome to Fitness Centre Management System --- ")
        print("1. Add Member")
        print("2. View All Members")
        print("3. Update Member Details")
        print("4. Delete Member")
        print("5. Search Member by Name")
        print("6. Total Members Count")
        print("7. Membership Type Count")
        print("8. Exit")

        choice = input("Enter Your Choice: ")
        if choice == '1':
            add_member()
        elif choice == '2':
            view_members()
        elif choice == '3':
            update_member()
        elif choice == '4':
            delete_member()
        elif choice == '5':
            search_member_by_name()
        elif choice == '6':
            total_members()
        elif choice == '7':
            membership_type_count()
        elif choice == '8':
            print('\nExiting...Thankyou for accessing our "FITNESS CENTRE MANAGEMENT"')
            break
        else:
            print("Invalid Choice...Please Try Again")

# Runing the program
create_table()   # Table pehli baar automatically ban jayega
check_password()
menu()
