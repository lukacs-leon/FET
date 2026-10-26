#SETUP
from typing import Literal

import sqlite3
conn = sqlite3.connect('FET.db')
cursor = conn.cursor()

#PRE-SETTED COLORS

GREEN = "\033[32m"
RED =  "\033[31m"
RESET = "\033[0m"

def print_welcome():
    banner = f"""{GREEN}
 ██╗    ██╗███████╗██╗      ██████╗ ███╗   ███╗███████╗    ████████╗ ██████╗     ███████╗███████╗████████╗
 ██║    ██║██╔════╝██║     ██╔════╝ ████╗ ████║██╔════╝    ╚══██╔══╝██╔═══██╗    ██╔════╝██╔════╝╚══██╔══╝
 ██║ █╗ ██║█████╗  ██║     ██║      ██╔████╔██║█████╗         ██║   ██║   ██║    █████╗  █████╗     ██║
 ██║███╗██║██╔══╝  ██║     ██║      ██║╚██╔╝██║██╔══╝         ██║   ██║   ██║    ██╔══╝  ██╔══╝     ██║
 ╚███╔███╔╝███████╗███████╗╚██████╗ ██║ ╚═╝ ██║███████╗       ██║   ╚██████╔╝    ██║     ███████╗   ██║
  ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝       ╚═╝    ╚═════╝     ╚═╝     ╚══════╝   ╚═╝
{GREEN} 'a place where you can transform your family life{RESET}
    """
    print(banner)

def SETUP():
    print_welcome()
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

#DEBUGING

def print_error(value, error=None):
    print(f"{RED}ERROR!")
    print(f"{value}")
    if error != None:
        print(f"{error}")
    else:
        print("No error explanation has given.")
    print(RESET)


#ADD

def add_user(user_id):
    cursor.execute("INSERT INTO users (user_id, current_balance) values (?, 0)", (user_id,))
    conn.commit()
    return

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

#CHECK

def check_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_existing = cursor.fetchone()
    return user_existing

def check_table(table):
    if table in ("users", "ledger"):
        return True
    else:
        print_error(value="Invalid table name!")

def check_add_type(add_type):
    if add_type in ("user", "point"):
        return True
    else:
        print_error(value="Incorrect add type")
        return

#GET

def get_input(text_to_ask):
    return input(text_to_ask)

#SEARCH

def search_in_users_by_id(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone()

#LISTING

def listing_table(table: Literal["users", "ledger"]):
    if check_table(table):
        data = read_table(table)
        for row in data:
            print(row)
    else:
        print_error(value="Incorrect table name!")












def read_table(table):
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    return data




def main():
    SETUP()
    try:
        while True:
            cmd = get_input("Write a command: (ls, add, search or exit) \n").lower()
            if cmd == "ls":
                table = get_input("Which table do you want list? (users / ledger) \n").lower()
                listing_table(table)
            elif cmd == "add":
                add_type = get_input("What do you want to add? user / point? \n").lower()
                if add_type in ("user", "point"):
                    if add_type == "user":
                        user_id = get_input("What is the user name? (This get_input is case sensitive!) \n")
                        add_user(user_id)
                    if add_type == "point":
                        user_id = get_input("What is the user name? (This get_input is case sensitive!) \n")
                        points = get_input("How much point do you want to add? (If you want to deduct, just write a minus) \n")
                        reason = get_input("What is the reason? \n")
                        try:
                            points = int(points)
                        except:
                            print(f"Something went wrong, with the value points ({points})")
                        add_points(user_id, points, reason)
            elif cmd == "search":
                search_type = get_input("Where do you want to search? users / ledger? \n").lower()
                if search_type in ("users", "ledger"):
                    if search_type == "users":
                        search_by_what = get_input("What do you want to search by? \n 1 => user_id \n 2 => current balance \n 3 => both \n")
                        if search_by_what in ("1", "2", "3"):
                            if search_by_what == "1":
                                search_for_user_id = get_input("What user ID do you look for? (this is case sensitive) \n")
                                print(search_in_users_by_id(search_for_user_id))
                            elif search_by_what == "2":
                                pass
                            elif search_by_what == "3":
                                pass
                        else:
                            print_error(value=f"Incorrect value! ({search_by_what})")
                    if search_type == "ledger":
                        print("Didn't made yet!")
                else:
                    print_error(f"incorrect value! ({search_type})")
            elif cmd == "exit":
                break
            else:
                print("Unavailable comand!")
    except Exception as e:
        print_error(error=e)
        conn.close()


#RUNNING
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