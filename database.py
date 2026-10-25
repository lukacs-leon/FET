import sqlite3
conn = sqlite3.connect('FET.db')
cursor = conn.cursor()

def get_input(text_to_ask):
    return input(text_to_ask)

def print_error(value, error=None):
    print(f"\033[31m {value} \033[0m")

def check_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_existing = cursor.fetchone()
    return user_existing

def add_points(user_id, points, reason):
    cursor.execute(
        """
        INSERT INTO ledger (user_id, points, reason) values (?, ?, ?)
        """,
        (user_id, points, reason),
    )
    user_existing = check_user(user_id)
    if user_existing != None:
        cursor.execute(
            "UPDATE users SET current_balance = current_balance + ? WHERE user_id = ?", 
            (points, user_id),
        )
        conn.commit()
    else:
        add_user(user_id)
    return

def read_table(table):
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    return data

def add_user(user_id):
    cursor.execute("INSERT INTO users (user_id, current_balance) values (?, 0)", (user_id,))
    conn.commit()
    return

def search_in_users_by_id(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone()

def main():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        current_balance INTEGER
        )
        """,
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ledger (
        x_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        points INTEGER,
        reason TEXT
        )
        """,
    )
    commander()

def commander():
    try:
        while True:
            cmd = input("Write a command: (ls, add, search or exit) \n").lower()
            if cmd == "ls":
                table = input("Which table do you want list? (users / ledger) \n").lower()
                if table in ("users", "ledger"):
                    data = read_table(table)
                    for row in data:
                        print(row)
                else:
                    print("INVALID TABLE NAME!")
            elif cmd == "add":
                add_type = input("What do you want to add? user / point? \n").lower()
                if add_type in ("user", "point"):
                    if add_type == "user":
                        user_id = input("What is the user name? (This input is case sensitive!) \n")
                        add_user(user_id)
                    if add_type == "point":
                        user_id = input("What is the user name? (This input is case sensitive!) \n")
                        points = input("How much point do you want to add? (If you want to deduct, just write a minus) \n")
                        reason = input("What is the reason? \n")
                        try:
                            points = int(points)
                        except:
                            print(f"Something went wrong, with the value points ({points})")
                        add_points(user_id, points, reason)
            elif cmd == "search":
                search_type = input("Where do you want to search? users / ledger? \n").lower()
                if search_type in ("users", "ledger"):
                    if search_type == "users":
                        search_by_what = input("What do you want to search by? \n 1 => user_id \n 2 => current balance \n 3 => both \n")
                        if search_by_what in ("1", "2", "3"):
                            if search_by_what == "1":
                                search_for_user_id = input("What user ID do you look for? (this is case sensitive) \n")
                                print(search_in_users_by_id(search_for_user_id))
                            elif search_by_what == "2":
                                pass
                            elif search_by_what == "3":
                                pass
                        else:
                            print(f"ERROR, incorrect value! ({search_by_what})")
                    if search_type == "ledger":
                        print("Didn't made yet!")
                else:
                    print(f"ERROR, incorrect value! ({search_type})")
            elif cmd == "exit":
                break
            else:
                print("Unavailable comand!")
    except Exception as e:
        print("ERROR! \n")
        print(e)
        conn.close()
        
        

main()
"""
add_points(user_id="LEON_42", points=+30, reason="jól kódol")

rows = read_table("users")
for row in rows:
    print(row)
print("="*50)
rows = read_table("ledger")
for row in rows:
    print(row)
"""