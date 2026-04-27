def view_paginated(cursor):
    page = 0
    page_size = 5
    while True:
        
        contacts = get_contacts_paginated(cursor, limit=page_size, offset=page * page_size)
        
        if not contacts:
            print("No more records.")
        else:
            for c in contacts:
                print(f"{c['first_name']} | {c['email']} | {c['group_name']}")
        
        cmd = input("\n[n]ext, [p]rev, [q]uit: ").lower()
        if cmd == 'n': page += 1
        elif cmd == 'p': page = max(0, page - 1)
        elif cmd == 'q': break