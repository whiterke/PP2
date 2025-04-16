import psycopg2
import csv

conn = psycopg2.connect(
    host="localhost",
    database="PhoneBook",
    user="qurmanbek"
)
cur = conn.cursor()

def insert_from_console():
    while True:
        name = input("Enter name (or type 'exit' to stop): ")
        if name.lower() == 'exit':
            break
        phone = input("Enter phone number: ")
        cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        print(f"✅ {name} has been saved!\n")

def insert_from_csv():
    path = input("Enter CSV file path (e.g. contacts.csv): ")
    try:
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                            (row['name'], row['phone']))
        conn.commit()
        print("✅ Data imported from CSV!")
    except Exception as e:
        print("❌ Error:", e)

def update_contact():
    name = input("Enter the name to update: ")
    new_phone = input("Enter the new phone number: ")
    cur.execute("UPDATE contacts SET phone = %s WHERE name = %s", (new_phone, name))
    conn.commit()
    print(f"🔄 Updated phone number for {name}")

def delete_contact():
    name = input("Enter the name to delete: ")
    cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
    conn.commit()
    print(f"❌ Deleted contact with name: {name}")

def show_all_contacts():
    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    print("\n📞 PhoneBook records:")
    for row in rows:
        print(row)

while True:
    print("\n===== PhoneBook Menu =====")
    print("1. Add contact manually")
    print("2. Import from CSV file")
    print("3. Update phone number")
    print("4. Delete contact")
    print("5. Show all contacts")
    print("0. Exit")

    choice = input("Select option: ")

    if choice == "1":
        insert_from_console()
    elif choice == "2":
        insert_from_csv()
    elif choice == "3":
        update_contact()
    elif choice == "4":
        delete_contact()
    elif choice == "5":
        show_all_contacts()
    elif choice == "0":
        break
    else:
        print("❗ Invalid choice")

cur.close()
conn.close()