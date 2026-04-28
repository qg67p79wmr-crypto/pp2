"""
phonebook.py  –  PhoneBook Extended (TSIS 1)
Builds on the CRUD / CSV / search / pagination foundations from
Practice 7 & 8.
"""

import csv
import json
import os
import sys
from datetime import date, datetime

import psycopg2
import psycopg2.extras


try:
    from connect import get_connection
except ImportError:
    print("Ошибка: Не найден файл connect.py рядом со скриптом!")

def _conn():
    return get_connection()

def _fmt_date(d):
    return d.isoformat() if d else ""

def _parse_date(s):
    """Преобразование строки в объект даты."""
    s = (s or "").strip()
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        print(f"  ⚠  Неверный формат даты '{s}' – ожидается YYYY-MM-DD.")
        return None

def _print_contacts(rows):
    """Красивый вывод списка контактов."""
    if not rows:
        print("  (контакты не найдены)")
        return
    sep = "-" * 80
    print(sep)
    for r in rows:
        phones = r.get("phones", [])
        phone_str = ", ".join(
            f"{p['phone']} [{p['type']}]" for p in phones
        ) if phones else "(нет номеров)"
        print(
            f"  [{r['id']:>4}]  {r['first_name']} {r.get('last_name') or ''}\n"
            f"         📧 {r.get('email') or '—'} "
            f"  🎂 {_fmt_date(r.get('birthday')) or '—'} "
            f"  👥 {r.get('group_name') or '—'}\n"
            f"         📞 {phone_str}"
        )
    print(sep)

def _fetch_contacts_with_phones(conn, contact_ids):
    """Загрузка контактов вместе с их номерами телефонов по ID."""
    if not contact_ids:
        return []
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            """
            SELECT c.id, c.first_name, c.last_name, c.email, c.birthday,
                   g.name AS group_name
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            WHERE c.id = ANY(%s)
            """,
            (list(contact_ids),),
        )
        contacts = {r["id"]: dict(r) for r in cur.fetchall()}

        cur.execute(
            "SELECT contact_id, phone, type FROM phones WHERE contact_id = ANY(%s)",
            (list(contact_ids),),
        )
        for row in cur.fetchall():
            contacts[row["contact_id"]].setdefault("phones", []).append(
                {"phone": row["phone"], "type": row["type"]}
            )

    for c in contacts.values():
        c.setdefault("phones", [])
    return [contacts[cid] for cid in contact_ids if cid in contacts]

def init_schema():
    """Создание таблиц и процедур из .sql файлов."""
    base = os.path.dirname(os.path.abspath(__file__))
    with _conn() as conn:
        with conn.cursor() as cur:
            for fname in ("schema.sql", "procedures.sql"):
                fpath = os.path.join(base, fname)
                if os.path.exists(fpath):
                    with open(fpath, encoding="utf-8") as f:
                        sql = f.read()
                    cur.execute(sql)
                    print(f"✅  Файл {fname} применен.")
                else:
                    print(f"  ⚠  Файл {fname} не найден в папке!")
        conn.commit()
    print("✅  База данных готова к работе.")

def filter_by_group():
    """Фильтрация контактов по группе."""
    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id, name FROM groups ORDER BY name")
            groups = cur.fetchall()

    if not groups:
        print("Группы не найдены.")
        return

    print("\nДоступные группы:")
    for g in groups:
        print(f"  {g['id']}. {g['name']}")
    choice = input("Введите номер или название группы: ").strip()

    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if choice.isdigit():
                cur.execute("SELECT id FROM contacts WHERE group_id = %s", (int(choice),))
            else:
                cur.execute(
                    "SELECT c.id FROM contacts c JOIN groups g ON g.id = c.group_id WHERE LOWER(g.name) = LOWER(%s)",
                    (choice,),
                )
            ids = [r["id"] for r in cur.fetchall()]
        results = _fetch_contacts_with_phones(conn, ids)
    _print_contacts(results)

def search_by_email():
    """Поиск по частичному совпадению email."""
    query = input("Введите email для поиска: ").strip()
    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id FROM contacts WHERE LOWER(email) LIKE %s", (f"%{query.lower()}%",))
            ids = [r["id"] for r in cur.fetchall()]
        results = _fetch_contacts_with_phones(conn, ids)
    _print_contacts(results)

def sort_and_list():
    """Сортировка контактов."""
    print("\nСортировать по: 1) Имени  2) Дате рождения  3) Дате добавления")
    choice = input("Выбор [1]: ").strip() or "1"
    order_map = {"1": "first_name, last_name", "2": "birthday NULLS LAST", "3": "id"}
    order = order_map.get(choice, "first_name")

    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(f"SELECT id FROM contacts ORDER BY {order}")
            ids = [r["id"] for r in cur.fetchall()]
        results = _fetch_contacts_with_phones(conn, ids)
    _print_contacts(results)

def paginated_browse():
    page_size = 5
    page = 0

    while True:
        offset = page * page_size

        with _conn() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                
                
                cur.execute(
                    "SELECT id FROM get_contacts_paginated(%s, %s)",
                    (page_size, offset)
                )
                ids = [r["id"] for r in cur.fetchall()]

            results = _fetch_contacts_with_phones(conn, ids)

        print(f"\n── Страница {page + 1} ──")
        _print_contacts(results)

        cmd = input("[N]ext  [P]rev  [Q]uit: ").strip().lower()
        if cmd == "n":
            page += 1
        elif cmd == "p":
            page = max(0, page - 1)
        elif cmd == "q":
            break
def export_to_json(filepath="contacts_export.json"):
    """Экспорт базы в JSON файл."""
    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id FROM contacts")
            ids = [r["id"] for r in cur.fetchall()]
        contacts = _fetch_contacts_with_phones(conn, ids)

    for c in contacts:
        if isinstance(c.get("birthday"), date):
            c["birthday"] = c["birthday"].isoformat()

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)
    print(f"✅  Экспортировано {len(contacts)} контактов в '{filepath}'.")

def _upsert_contact_from_dict(conn, data, on_duplicate="ask"):
    """Вставка или обновление контакта."""
    first = (data.get("first_name") or "").strip()
    last = (data.get("last_name") or "").strip() or None
    if not first: return

    with conn.cursor() as cur:
        cur.execute("SELECT id FROM contacts WHERE first_name=%s AND (last_name=%s OR last_name IS NULL)", (first, last))
        existing = cur.fetchone()

    if existing:
        action = on_duplicate
        if action == "ask":
            print(f"  ⚠  Дубликат: '{first} {last or ''}'. Перезаписать? [y/n]: ", end="")
            action = "overwrite" if input().lower() == "y" else "skip"
        if action == "skip": return
        with conn.cursor() as cur:
            cur.execute("DELETE FROM contacts WHERE id = %s", (existing[0],))

    # Группа
    group_id = None
    group_name = (data.get("group_name") or data.get("group") or "").strip()
    if group_name:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (group_name,))
            cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            group_id = cur.fetchone()[0]

    birthday = _parse_date(data.get("birthday"))
    email = data.get("email")

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO contacts (first_name, last_name, email, birthday, group_id) VALUES (%s,%s,%s,%s,%s) RETURNING id",
            (first, last, email, birthday, group_id)
        )
        c_id = cur.fetchone()[0]
        
        phones = data.get("phones", [])
        if not phones and data.get("phone"):
            phones = [{"phone": data["phone"], "type": data.get("phone_type", "mobile")}]
        
        for p in phones:
            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)", (c_id, p["phone"], p.get("type", "mobile")))
    conn.commit()
    print(f"  ✅ Сохранено: {first} {last or ''}")

def import_from_json():
    """Загрузка из JSON."""
    path = input("Путь к JSON [contacts.json]: ").strip() or "contacts.json"
    if not os.path.exists(path):
        print("Файл не найден!")
        return
    with open(path, encoding="utf-8") as f:
        records = json.load(f)
    with _conn() as conn:
        for r in records:
            _upsert_contact_from_dict(conn, r, on_duplicate="ask")
    print("✅ Импорт завершен.")
def import_from_csv():
    path = input("Путь к CSV [contacts.csv]: ").strip() or "contacts.csv"

    if not os.path.exists(path):
        print("Файл не найден!")
        return

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        with _conn() as conn:
            for row in reader:
                data = {
                    "first_name": row.get("first_name"),
                    "last_name": row.get("last_name"),
                    "email": row.get("email"),
                    "birthday": row.get("birthday"),
                    "group_name": row.get("group"),
                    "phones": [
                        {
                            "phone": row.get("phone"),
                            "type": row.get("type", "mobile")
                        }
                    ] if row.get("phone") else []
                }

                _upsert_contact_from_dict(conn, data, on_duplicate="ask")

    print("✅ CSV импорт завершён.")

def call_add_phone():
    name = input("Имя контакта: ").strip()
    phone = input("Номер: ").strip()
    with _conn() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL add_phone(%s, %s, 'mobile')", (name, phone))
        conn.commit()
    print("✅ Номер добавлен через процедуру.")

MENU = """
--- ТЕЛЕФОННАЯ КНИГА (TSIS 1) ---
1. Импорт из JSON
2. Фильтр по группе
3. Поиск по Email
4. Сортировка и список
5. Постраничный просмотр (Pagination)
6. Экспорт в JSON
7. Добавить телефон (Procedure)
i. Инициализировать таблицы (Init Schema)
8. Импорт из CSV
q. Выход
"""

HANDLERS = {
    "1": import_from_json,
    "2": filter_by_group,
    "3": search_by_email,
    "4": sort_and_list,
    "5": paginated_browse,
    "6": export_to_json,
    "7": call_add_phone,
    "i": init_schema,
    "8": import_from_csv
}

def main():
    while True:
        print(MENU)
        choice = input("Выбери пункт: ").strip().lower()
        if choice == "q": break
        handler = HANDLERS.get(choice)
        if handler:
            try:
                handler()
            except Exception as e:
                print(f"Ошибка: {e}")
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()