import psycopg2
import csv

def connect():
    return psycopg2.connect(
        host="localhost",
        database="phonebook_db",
        user="postgres",
        password="1234"
    )

def insert_from_csv(csv_path):
    conn = connect()
    cur = conn.cursor()
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING", (row[0], row[1]))
    conn.commit()
    cur.close()
    conn.close()
    print("CSV data inserted successfully.")

def insert_from_console():
    conn = connect()
    cur = conn.cursor()
    first_name = input("Enter first name: ")
    phone = input("Enter phone number: ")
    cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING", (first_name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact inserted successfully.")

def update_phonebook(username, new_name=None, new_phone=None):
    conn = connect()
    cur = conn.cursor()
    if new_name:
        cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, username))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone = %s WHERE first_name = %s", (new_phone, username))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated successfully.")

def query_phonebook(name_filter=None, phone_filter=None):
    conn = connect()
    cur = conn.cursor()
    if name_filter:
        cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f"%{name_filter}%",))
    elif phone_filter:
        cur.execute("SELECT * FROM phonebook WHERE phone ILIKE %s", (f"%{phone_filter}%",))
    else:
        cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def delete_entry(name=None, phone=None):
    conn = connect()
    cur = conn.cursor()
    if name:
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
    if phone:
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted successfully.")

# ==== MENU ====
def menu():
    while True:
        print("\n=== PhoneBook Menu ===")
        print("1. Insert from CSV")
        print("2. Insert from Console")
        print("3. View All Contacts")
        print("4. Search by Name")
        print("5. Search by Phone")
        print("6. Update Contact")
        print("7. Delete by Name")
        print("8. Delete by Phone")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            path = input("Enter CSV file path: ")
            insert_from_csv(path)
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            query_phonebook()
        elif choice == "4":
            name = input("Enter name to search: ")
            query_phonebook(name_filter=name)
        elif choice == "5":
            phone = input("Enter phone to search: ")
            query_phonebook(phone_filter=phone)
        elif choice == "6":
            name = input("Enter existing name to update: ")
            new_name = input("New name (press enter to skip): ")
            new_phone = input("New phone (press enter to skip): ")
            update_phonebook(name, new_name if new_name else None, new_phone if new_phone else None)
        elif choice == "7":
            name = input("Enter name to delete: ")
            delete_entry(name=name)
        elif choice == "8":
            phone = input("Enter phone to delete: ")
            delete_entry(phone=phone)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

# Start the menu
if __name__ == "__main__":
    menu()

