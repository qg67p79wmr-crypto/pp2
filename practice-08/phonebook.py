from connect import get_connection



def search():
    pattern = input("Enter pattern: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()



def upsert():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
    conn.commit()

    print("Done")

    cur.close()
    conn.close()



def bulk_insert():
    names = input("Enter names (comma): ").split(",")
    phones = input("Enter phones (comma): ").split(",")

    names = [n.strip() for n in names]
    phones = [p.strip() for p in phones]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL insert_many_contacts(%s, %s);", (names, phones))
    conn.commit()

    print("Bulk insert done")

    cur.close()
    conn.close()



def pagination():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()



def delete():
    value = input("Enter username or phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s);", (value,))
    conn.commit()

    print("Deleted")

    cur.close()
    conn.close()



def show_all():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook;")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()



def menu():
    while True:
        print("\n--- PRACTICE 8 ---")
        print("1. Search")
        print("2. Upsert")
        print("3. Bulk insert")
        print("4. Pagination")
        print("5. Delete")
        print("6. Show all")
        print("0. Exit")

        choice = input("Choice: ")

        if choice == "1":
            search()
        elif choice == "2":
            upsert()
        elif choice == "3":
            bulk_insert()
        elif choice == "4":
            pagination()
        elif choice == "5":
            delete()
        elif choice == "6":
            show_all()
        elif choice == "0":
            break
        else:
            print("Invalid")


menu()