from typing import Literal
import sqlite3

conn = sqlite3.connect('FET.db')
cursor = conn.cursor()

#PRE-SETTED COLORS

GREEN = "\033[32m"
RED =  "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

#STARTING FUNCTIONS

def print_welcome():
    banner = f"""{GREEN}
 ██╗    ██╗███████╗██╗      ██████╗ ███╗   ███╗███████╗    ████████╗ ██████╗     ███████╗███████╗████████╗
 ██║    ██║██╔════╝██║     ██╔════╝ ████╗ ████║██╔════╝    ╚══██╔══╝██╔═══██╗    ██╔════╝██╔════╝╚══██╔══╝
 ██║ █╗ ██║█████╗  ██║     ██║      ██╔████╔██║█████╗         ██║   ██║   ██║    █████╗  █████╗     ██║
 ██║███╗██║██╔══╝  ██║     ██║      ██║╚██╔╝██║██╔══╝         ██║   ██║   ██║    ██╔══╝  ██╔══╝     ██║
 ╚███╔███╔╝███████╗███████╗╚██████╗ ██║ ╚═╝ ██║███████╗       ██║   ╚██████╔╝    ██║     ███████╗   ██║
  ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝       ╚═╝    ╚═════╝     ╚═╝     ╚══════╝   ╚═╝
{GREEN} a place where you can transform your family life{RESET}
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

def print_error(text, error=None):
    print(f"{RED}ERROR!")
    print(f"{text}")
    if error != None:
        print(f"{error}")
    else:
        print("No error explanation has given.")
    print(RESET)

def print_warning(text):
    print(f"{YELLOW}{text}{RESET}")

# UNIVERSAL ROBUST INPUT HANDLER
def get_valid_input(prompt_text, input_type="str", allow_empty=False):
    while True:
        raw_val = input(f"{prompt_text} \n")
        
        if raw_val.strip().lower() == "break":
            return "BREAK"
            
        if raw_val.strip() == "":
            if allow_empty:
                return None
            else:
                return "BREAK"
                
        if input_type == "int":
            try:
                return int(raw_val)
            except ValueError:
                print_error(f"Invalid number format: '{raw_val}'. Please enter a valid integer (or type 'break').")
                continue
                
        return raw_val

#ADD (Exact match required here)

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
    cursor.execute(
        "UPDATE users SET current_balance = current_balance + ? WHERE user_id = ?", 
        (points, user_id),
    )
    conn.commit()
    return

#CHECK

def check_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_existing = cursor.fetchone()
    return user_existing

def check_table(table: Literal["users", "ledger"]):
    if table in ("users", "ledger"):
        return True
    else:
        print_error("Invalid table name!")
        return

def check_add_type(add_type: Literal["users", "point"]):
    if add_type in ("user", "point"):
        return True
    else:
        print_error("Incorrect add type")
        return

def check_search_type(search_type):
    if search_type in ("users", "ledger"):
        return True
    else:
        print_error(f"Incorrect search type! {search_type}")
        return

def check_search_by_what_at_users(search_by_what_at_users):
    if search_by_what_at_users in ("1", "2", "3", "user_id", "current balance", "conditions"):
        return True
    else:
        print_error(f"Incorrect search by what at users ({search_by_what_at_users})")
        return

def check_search_by_what_at_ledger(check_search_by_what_at_ledger):
    if check_search_by_what_at_ledger in ("1", "2", "3", "4", "user_id", "points", "reason", "conditions"):
        return True
    else:
        print_error(f"Incorrect search by what at ledger ({check_search_by_what_at_ledger})")
        return

#GET

def get_table_data(table):
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    return data

#SEARCH (Flexible LIKE search for user_id across all search functions)

def search_in_users_by_id(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id LIKE ?", (f"%{user_id}%",))
    return cursor.fetchall()

def search_in_users_by_balance(balance):
    cursor.execute("SELECT * FROM users WHERE current_balance = ?", (balance,))
    return cursor.fetchall()

def search_in_ledger_by_keywords(keywords):
    if not keywords:
        return []
    
    clauses = []
    params = []
    
    for kw in keywords:
        clauses.append("reason LIKE ?")
        params.append(f"%{kw}%")
    
    sql_query = f"SELECT * FROM ledger WHERE {' OR '.join(clauses)}"
    cursor.execute(sql_query, tuple(params))
    return cursor.fetchall()

def search_in_ledger_by_user_id(user_id):
    cursor.execute("SELECT * FROM ledger WHERE user_id LIKE ?", (f"%{user_id}%",))
    return cursor.fetchall()

def search_in_ledger_by_point(point):
    cursor.execute("SELECT * FROM ledger WHERE points = ?", (point,))
    return cursor.fetchall()

def search_in_users_with_conditions(user_id=None, min_balance=None, max_balance=None):
    sql_query = "SELECT * FROM users WHERE 1=1"
    params = []
    
    if user_id:
        sql_query += " AND user_id LIKE ?"
        params.append(f"%{user_id}%")
        
    if min_balance is not None:
        sql_query += " AND current_balance >= ?"
        params.append(min_balance)
        
    if max_balance is not None:
        sql_query += " AND current_balance <= ?"
        params.append(max_balance)
        
    cursor.execute(sql_query, tuple(params))
    return cursor.fetchall()

def search_in_ledger_with_conditions(user_id=None, min_points=None, max_points=None, keywords=None):
    sql_query = "SELECT * FROM ledger WHERE 1=1"
    params = []
    
    if user_id:
        sql_query += " AND user_id LIKE ?"
        params.append(f"%{user_id}%")
        
    if min_points is not None:
        sql_query += " AND points >= ?"
        params.append(min_points)
        
    if max_points is not None:
        sql_query += " AND points <= ?"
        params.append(max_points)
        
    if keywords:
        clauses = []
        for kw in keywords:
            clauses.append("reason LIKE ?")
            params.append(f"%{kw}%")
        sql_query += f" AND ({' OR '.join(clauses)})"
        
    cursor.execute(sql_query, tuple(params))
    return cursor.fetchall()

#LISTING

def list_table(table: Literal["users", "ledger"]):
    if check_table(table):
        data = get_table_data(table)
        print_output_row_by_row(data)
    else:
        print_error("Incorrect table name!")
        return

#OUTPUT PRINTER

def print_output_row_by_row(data):
    if not data:
        print_warning("No results found.")
        return
    for row in data:
        print(row)


def main():
    SETUP()
    try:
        while True:
            cmd = get_valid_input("Write a command: (ls, add, search or exit)", input_type="str", allow_empty=False)
            if cmd == "BREAK":
                break
            cmd = cmd.lower()
            
            if cmd == "ls":
                table = get_valid_input("Which table do you want to list? (users / ledger) [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False)
                if table == "BREAK":
                    continue
                if check_table(table):
                    list_table(table)
                else:
                    print_error(f"Incorrect table name: {table}")
                    continue
                    
            elif cmd == "add":
                add_type = get_valid_input("What do you want to add? user / point? [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False)
                if add_type == "BREAK":
                    continue
                add_type = add_type.lower()
                
                if check_add_type(add_type):
                    if add_type == "user":
                        user_id = get_valid_input("What is the user name? (Case sensitive) [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False)
                        if user_id == "BREAK":
                            continue
                        add_user(user_id)
                        print(f"{GREEN}User '{user_id}' added successfully!{RESET}")
                        
                    elif add_type == "point":
                        user_id = get_valid_input("What is the user name? [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False)
                        if user_id == "BREAK":
                            continue
                        
                        user_existing = check_user(user_id)
                        if user_existing is None:
                            print_warning(f"User '{user_id}' does not exist.")
                            create_choice = get_valid_input(f"Do you want to create user '{user_id}' now? (y/n) [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False).lower()
                            
                            if create_choice == "break" or create_choice == "BREAK":
                                continue
                            
                            if create_choice in ("y", "yes"):
                                add_user(user_id)
                                print(f"{GREEN}User '{user_id}' created successfully!{RESET}")
                            else:
                                print_warning("Operation cancelled. User was not created.")
                                continue
                        
                        points = get_valid_input("How many points do you want to add? (Deduction: use minus) [Type 'break' or press Enter to cancel]", input_type="int")
                        if points == "BREAK":
                            continue
                            
                        reason = get_valid_input("What is the reason? [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False)
                        if reason == "BREAK":
                            continue
                            
                        add_points(user_id, points, reason)
                        print(f"{GREEN}Successfully added {points} points to '{user_id}'!{RESET}")
                        
            elif cmd == "search":
                search_type = get_valid_input("Where do you want to search? users / ledger? [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False).lower()
                if search_type == "BREAK":
                    continue
                    
                if check_search_type(search_type):
                    if search_type == "users":
                        search_by_what_at_users = get_valid_input("What do you want to search by? \n 1 => user_id \n 2 => current balance \n 3 => conditions \n [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False).lower()
                        if search_by_what_at_users == "BREAK":
                            continue
                            
                        if check_search_by_what_at_users(search_by_what_at_users):
                            if search_by_what_at_users in ("1", "user_id"):
                                search_for_user_id = get_valid_input("What user ID do you look for? [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False)
                                if search_for_user_id == "BREAK":
                                    continue
                                print_output_row_by_row(search_in_users_by_id(search_for_user_id))
                                
                            elif search_by_what_at_users in ("2", "current balance"):
                                balance = get_valid_input("What balance are you looking for? [Type 'break' or press Enter to cancel]", input_type="int")
                                if balance == "BREAK":
                                    continue
                                print_output_row_by_row(search_in_users_by_balance(balance))
                                
                            elif search_by_what_at_users in ("3", "conditions"):
                                print_warning("Leave blank (Press Enter) if you don't want to filter by that condition. Type 'break' to cancel.")
                                
                                u_id = get_valid_input("Filter by user_id keyword (Enter to skip):", input_type="str", allow_empty=True)
                                if u_id == "BREAK":
                                    continue
                                
                                min_bal_str = get_valid_input("Filter by minimum current_balance (Enter to skip):", input_type="str", allow_empty=True)
                                if min_bal_str == "BREAK":
                                    continue
                                    
                                max_bal_str = get_valid_input("Filter by maximum current_balance (Enter to skip):", input_type="str", allow_empty=True)
                                if max_bal_str == "BREAK":
                                    continue
                                
                                u_id_param = u_id if u_id else None
                                min_bal_param = int(min_bal_str) if min_bal_str else None
                                max_bal_param = int(max_bal_str) if max_bal_str else None
                                        
                                results = search_in_users_with_conditions(
                                    user_id=u_id_param, 
                                    min_balance=min_bal_param, 
                                    max_balance=max_bal_param
                                )
                                print_output_row_by_row(results)
                        else:
                            print_error(f"Incorrect value! ({search_by_what_at_users})")
                            continue
                            
                    elif search_type == "ledger":
                        search_by_what_at_ledger = get_valid_input("What do you want to search by? \n 1 => user_id \n 2 => points \n 3 => reason \n 4 => conditions \n [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False).lower()
                        if search_by_what_at_ledger == "BREAK":
                            continue
                            
                        if check_search_by_what_at_ledger(search_by_what_at_ledger):
                            if search_by_what_at_ledger in ("1", "user_id"):
                                user_id = get_valid_input("What user ID do you look for? [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False)
                                if user_id == "BREAK":
                                    continue
                                print_output_row_by_row(search_in_ledger_by_user_id(user_id))
                                
                            elif search_by_what_at_ledger in ("2", "points"):
                                points = get_valid_input("What points do you look for? [Type 'break' or press Enter to cancel]", input_type="int")
                                if points == "BREAK":
                                    continue
                                print_output_row_by_row(search_in_ledger_by_point(points))
                                
                            elif search_by_what_at_ledger in ("3", "reason"):
                                keywords = []
                                print_warning("Type keywords one by one. Press Enter on empty line to finish, or type 'break' to cancel.")
                                while True:
                                    kw = get_valid_input("Add a keyword (Enter to finish):", input_type="str", allow_empty=True)
                                    if kw == "BREAK":
                                        keywords = []
                                        break
                                    if kw is None or kw == "":
                                        break
                                    keywords.append(kw)
                                if keywords:
                                    print_output_row_by_row(search_in_ledger_by_keywords(keywords))
                                    
                            elif search_by_what_at_ledger in ("4", "conditions"):
                                print_warning("Leave blank (Press Enter) if you don't want to filter by that condition. Type 'break' to cancel.")
                                
                                u_id = get_valid_input("Filter by user_id keyword (Enter to skip):", input_type="str", allow_empty=True)
                                if u_id == "BREAK":
                                    continue
                                    
                                min_p_str = get_valid_input("Filter by minimum points (Enter to skip):", input_type="str", allow_empty=True)
                                if min_p_str == "BREAK":
                                    continue
                                    
                                max_p_str = get_valid_input("Filter by maximum points (Enter to skip):", input_type="str", allow_empty=True)
                                if max_p_str == "BREAK":
                                    continue
                                    
                                u_id_param = u_id if u_id else None
                                min_p_param = int(min_p_str) if min_p_str else None
                                max_p_param = int(max_p_str) if max_p_str else None
                                        
                                keywords = []
                                add_kw = get_valid_input("Do you want to filter by reason keywords? (y/n)", input_type="str", allow_empty=False).lower()
                                if add_kw == "y":
                                    while True:
                                        kw = get_valid_input("Add a keyword (Enter to finish):", input_type="str", allow_empty=True)
                                        if kw is None or kw == "":
                                            break
                                        keywords.append(kw)
                                        
                                results = search_in_ledger_with_conditions(
                                    user_id=u_id_param, 
                                    min_points=min_p_param, 
                                    max_points=max_p_param, 
                                    keywords=keywords if keywords else None
                                )
                                print_output_row_by_row(results)
                else:
                    print_error(f"incorrect value! ({search_type})")
                    continue
            elif cmd == "exit":
                break
            else:
                print_error("Unavailable command!")
    except Exception as e:
        print_error(error=e)

#RUNNING
main()