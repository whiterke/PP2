import psycopg2
import csv
import sys

DSN = {
    'host':     'localhost',
    'database': 'phonebook_db',
    'user':     'postgres',
    'password': '1234'
}


def search_contacts(cur):
    pat = input("🔍 Enter search pattern: ").strip()
    cur.execute("SELECT * FROM search_contacts(%s)", (pat,))
    rows = cur.fetchall()
    if not rows:
        print("No matches found.")
    else:
        print("\nID | Name                 | Phone")
        print("---+----------------------+---------------")
        for _id, name, phone in rows:
            print(f"{_id:2d} | {name:20s} | {phone}")
    print()


def upsert_contact(cur, conn):
    name  = input("👤 Name: ").strip()
    phone = input("📞 Phone: ").strip()
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    print(f"✔️  Upserted: {name} → {phone}\n")


def batch_insert_from_csv(cur, conn):
    path = input("📁 CSV file path: ").strip()
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            inputs = [(r['name'], r['phone']) for r in reader]
    except Exception as e:
        print("❌ Failed to read CSV:", e)
        return

    if not inputs:
        print("❗ CSV is empty or missing 'name','phone' headers.")
        return

    # Build the CALL array literal
    rows_sql = ",".join("ROW(%s,%s)" for _ in inputs)
    sql = f"SELECT * FROM batch_insert_contacts(ARRAY[{rows_sql}]::contact_input[]);"
    params = [val for pair in inputs for val in pair]

    cur.execute(sql, params)
    bad = cur.fetchall()
    conn.commit()

    if bad:
        print("⚠️  Invalid entries (not inserted/updated):")
        for name, phone in bad:
            print(f"   • {name} → {phone}")
    else:
        print("✅ All rows inserted/updated successfully.")
    print()


def paginate_contacts(cur):
    try:
        lim    = int(input("Limit  (default 10): ").strip() or 10)
        offset = int(input("Offset (default 0): ").strip() or 0)
    except ValueError:
        print("❌ Please enter valid integers.")
        return

    cur.execute("SELECT * FROM paginate_contacts(%s, %s)", (lim, offset))
    rows = cur.fetchall()

    if not rows:
        print("No rows to show.")
    else:
        print(f"\nShowing up to {lim} rows starting at offset {offset}:")
        print("ID | Name                 | Phone")
        print("---+----------------------+---------------")
        for _id, name, phone in rows:
            print(f"{_id:2d} | {name:20s} | {phone}")
    print()


def delete_contact(cur, conn):
    name_pat  = input("Name pattern (ILIKE, e.g. '%Ivan%') or blank: ").strip() or None
    phone_pat = input("Phone pattern (ILIKE, e.g. '+7701%') or blank: ").strip() or None

    if not name_pat and not phone_pat:
        print("❗ Nothing to delete.\n")
        return

    cur.execute("CALL delete_contact_by(%s, %s)", (name_pat, phone_pat))
    conn.commit()
    print("🗑️  Delete operation completed.\n")


def main():
    try:
        conn = psycopg2.connect(**DSN)
    except Exception as e:
        print("❌ Could not connect to DB:", e)
        sys.exit(1)

    cur = conn.cursor()

    menu = """
===== PhoneBook CLI =====
1. Search contacts
2. Upsert contact (insert or update)
3. Batch‑insert from CSV
4. Paginate listing
5. Delete by name or phone
0. Exit
"""
    while True:
        print(menu)
        choice = input("Select option: ").strip()
        if choice == "1":
            search_contacts(cur)
        elif choice == "2":
            upsert_contact(cur, conn)
        elif choice == "3":
            batch_insert_from_csv(cur, conn)
        elif choice == "4":
            paginate_contacts(cur)
        elif choice == "5":
            delete_contact(cur, conn)
        elif choice == "0":
            break
        else:
            print("❗ Invalid choice. Try again.\n")

    cur.close()
    conn.close()
    print("👋 Goodbye!")


if __name__ == "__main__":
    main()
