import json

def export_to_json(cursor, filename="contacts.export.json"):
    query = """
        SELECT c.first_name, c.email, c.birthday, g.name as group_name,
               json_agg(json_build_object('phone', p.phone, 'type', p.type)) as phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, g.name;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    
    with open(filename, 'w') as f:
        json.dump(rows, f, indent=4, default=str)
    print(f"Exported to {filename}")

import json

def export_to_json(cursor):
    cursor.execute("SELECT first_name, email, birthday FROM contacts")
    rows = cursor.fetchall() 
    
   
    data = []
    for row in rows:
        data.append({
            "name": row[0],
            "email": row[1],
            "birthday": str(row[2])
        })
    
    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Данные сохранены в contacts.json")