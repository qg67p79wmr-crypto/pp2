import csv
import psycopg2
from connect import get_connection


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully.")


def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO phonebook (username, phone) VALUES (%s, %s);",
            (username, phone)
        )
        conn.commit()
        print("Contact added successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def insert_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()

    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if len(row) >= 2:
                    username, phone = row[0], row[1]
                    try:
                        cur.execute(
                            "INSERT INTO phonebook (username, phone) VALUES (%s, %s);",
                            (username, phone)
                        )
                        conn.commit()
                    except Exception:
                        conn.rollback()
                        continue

        print("Data inserted from CSV successfully.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def update_contact():
    print("1. Update username")
    print("2. Update phone")
    choice = input("Choose option: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        if choice == "1":
            old_username = input("Enter current username: ")
            new_username = input("Enter new username: ")

            cur.execute(
                "UPDATE phonebook SET username = %s WHERE username = %s;",
                (new_username, old_username)
            )

        elif choice == "2":
            username = input("Enter username: ")
            new_phone = input("Enter new phone: ")

            cur.execute(
                "UPDATE phonebook SET phone = %s WHERE username = %s;",
                (new_phone, username)
            )

        else:
            print("Invalid choice.")
            cur.close()
            conn.close()
            return

        conn.commit()
        print(f"Updated rows: {cur.rowcount}")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def query_all_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, username, phone FROM phonebook ORDER BY id;")
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


def query_by_name():
    pattern = input("Enter name or part of name: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username, phone FROM phonebook WHERE username ILIKE %s;",
        ("%" + pattern + "%",)
    )

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


def query_by_phone_prefix():
    prefix = input("Enter phone prefix: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username, phone FROM phonebook WHERE phone LIKE %s;",
        (prefix + "%",)
    )

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


def delete_by_username():
    username = input("Enter username to delete: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE username = %s;",
        (username,)
    )

    conn.commit()
    print(f"Deleted rows: {cur.rowcount}")

    cur.close()
    conn.close()


def delete_by_phone():
    phone = input("Enter phone to delete: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE phone = %s;",
        (phone,)
    )

    conn.commit()
    print(f"Deleted rows: {cur.rowcount}")

    cur.close()
    conn.close()


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Insert from console")
        print("3. Insert from CSV")
        print("4. Update contact")
        print("5. Show all contacts")
        print("6. Search by name")
        print("7. Search by phone prefix")
        print("8. Delete by username")
        print("9. Delete by phone")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            filename = input("Enter CSV filename: ")
            insert_from_csv(filename)
        elif choice == "4":
            update_contact()
        elif choice == "5":
            query_all_contacts()
        elif choice == "6":
            query_by_name()
        elif choice == "7":
            query_by_phone_prefix()
        elif choice == "8":
            delete_by_username()
        elif choice == "9":
            delete_by_phone()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


menu()