from typing import Literal
from database import FETDatabase

class FETCli:
    def __init__(self):
        self.db = FETDatabase()
        self.GREEN = "\033[32m"
        self.RED = "\033[31m"
        self.YELLOW = "\033[33m"
        self.RESET = "\033[0m"

    def print_welcome(self):
        banner = f"""{self.GREEN}
 ██╗    ██╗███████╗██╗      ██████╗ ███╗   ███╗███████╗    ████████╗ ██████╗     ███████╗███████╗████████╗
 ██║    ██║██╔════╝██║     ██╔════╝ ████╗ ████║██╔════╝    ╚══██╔══╝██╔═══██╗    ██╔════╝██╔════╝╚══██╔══╝
 ██║ █╗ ██║█████╗  ██║     ██║      ██╔████╔██║█████╗         ██║   ██║   ██║    █████╗  █████╗     ██║
 ██║███╗██║██╔══╝  ██║     ██║      ██║╚██╔╝██║██╔══╝         ██║   ██║   ██║    ██╔══╝  ██╔══╝     ██║
 ╚███╔███╔╝███████╗███████╗╚██████╗ ██║ ╚═╝ ██║███████╗       ██║   ╚██████╔╝    ██║     ███████╗   ██║
  ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝       ╚═╝    ╚═════╝     ╚═╝     ╚══════╝   ╚═╝
{self.GREEN} a place where you can transform your family life{self.RESET}
        """
        print(banner)

    def print_error(self, text, error=None):
        print(f"{self.RED}ERROR!")
        print(f"{text}")
        if error != None:
            print(f"{error}")
        else:
            print("No error explanation has given.")
        print(self.RESET)

    def print_warning(self, text):
        print(f"{self.YELLOW}{text}{self.RESET}")

    def get_valid_input(self, prompt_text, input_type="str", allow_empty=False):
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
                    self.print_error(f"Invalid number format: '{raw_val}'. Please enter a valid integer (or type 'break').")
                    continue
                    
            return raw_val

    def check_table(self, table: str):
        if table in ("users", "ledger"):
            return True
        else:
            self.print_error("Invalid table name!")
            return False

    def check_add_type(self, add_type: str):
        if add_type in ("user", "point"):
            return True
        else:
            self.print_error("Incorrect add type")
            return False

    def check_search_type(self, search_type: str):
        if search_type in ("users", "ledger"):
            return True
        else:
            self.print_error(f"Incorrect search type! {search_type}")
            return False

    def check_search_by_what_at_users(self, val: str):
        if val in ("1", "2", "3", "user_id", "current balance", "conditions"):
            return True
        else:
            self.print_error(f"Incorrect search by what at users ({val})")
            return False

    def check_search_by_what_at_ledger(self, val: str):
        if val in ("1", "2", "3", "4", "user_id", "points", "reason", "conditions"):
            return True
        else:
            self.print_error(f"Incorrect search by what at ledger ({val})")
            return False

    def print_output_row_by_row(self, data):
        if not data:
            self.print_warning("No results found.")
            return
        for row in data:
            print(row)

    def run(self):
        self.print_welcome()
        try:
            while True:
                cmd = self.get_valid_input("Write a command: (ls, add, search or exit)", input_type="str", allow_empty=False)
                if cmd == "BREAK":
                    break
                cmd = cmd.lower()
                
                if cmd == "ls":
                    table = self.get_valid_input("Which table do you want to list? (users / ledger) [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False)
                    if table == "BREAK":
                        continue
                    if self.check_table(table):
                        order_choice = self.get_valid_input("Order by? (1 => ID / Name, 2 => Balance/Points) [Enter to skip]", input_type="str", allow_empty=True)
                        order_field = "balance" if order_choice == "2" else "user_id"
                        
                        dir_choice = self.get_valid_input("Direction? (1 => ASC [Low->High / A-Z], 2 => DESC [High->Low / Z-A]) [Enter for ASC]", input_type="str", allow_empty=True)
                        direction = "DESC" if dir_choice == "2" else "ASC"
                        
                        data = self.db.get_table_data(table, order_by=order_field, direction=direction)
                        self.print_output_row_by_row(data)
                    else:
                        self.print_error(f"Incorrect table name: {table}")
                        continue
                        
                elif cmd == "add":
                    add_type = self.get_valid_input("What do you want to add? user / point? [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False)
                    if add_type == "BREAK":
                        continue
                    add_type = add_type.lower()
                    
                    if self.check_add_type(add_type):
                        if add_type == "user":
                            user_id = self.get_valid_input("What is the user name? (Case sensitive) [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False)
                            if user_id == "BREAK":
                                continue
                            self.db.add_user(user_id)
                            print(f"{self.GREEN}User '{user_id}' added successfully!{self.RESET}")
                            
                        elif add_type == "point":
                            user_id = self.get_valid_input("What is the user name? [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False)
                            if user_id == "BREAK":
                                continue
                            
                            user_existing = self.db.check_user(user_id)
                            if user_existing is None:
                                self.print_warning(f"User '{user_id}' does not exist.")
                                create_choice = self.get_valid_input(f"Do you want to create user '{user_id}' now? (y/n) [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False).lower()
                                
                                if create_choice in ("break", "BREAK"):
                                    continue
                                
                                if create_choice in ("y", "yes"):
                                    self.db.add_user(user_id)
                                    print(f"{self.GREEN}User '{user_id}' created successfully!{self.RESET}")
                                else:
                                    self.print_warning("Operation cancelled. User was not created.")
                                    continue
                            
                            points = self.get_valid_input("How many points do you want to add? (Deduction: use minus) [Type 'break' or press Enter to cancel]", input_type="int")
                            if points == "BREAK":
                                continue
                                
                            reason = self.get_valid_input("What is the reason? [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False)
                            if reason == "BREAK":
                                continue
                                
                            self.db.add_points(user_id, points, reason)
                            print(f"{self.GREEN}Successfully added {points} points to '{user_id}'!{self.RESET}")
                            
                elif cmd == "search":
                    search_type = self.get_valid_input("Where do you want to search? users / ledger? [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False).lower()
                    if search_type == "BREAK":
                        continue
                        
                    if self.check_search_type(search_type):
                        order_choice = self.get_valid_input("Order by? (1 => ID / Name, 2 => Balance/Points) [Enter to skip]", input_type="str", allow_empty=True)
                        order_field = "balance" if order_choice == "2" else "user_id"
                        
                        dir_choice = self.get_valid_input("Direction? (1 => ASC, 2 => DESC) [Enter for ASC]", input_type="str", allow_empty=True)
                        direction = "DESC" if dir_choice == "2" else "ASC"

                        if search_type == "users":
                            search_by_what_at_users = self.get_valid_input("What do you want to search by? \n 1 => user_id \n 2 => current balance \n 3 => conditions \n [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False).lower()
                            if search_by_what_at_users == "BREAK":
                                continue
                                
                            if self.check_search_by_what_at_users(search_by_what_at_users):
                                if search_by_what_at_users in ("1", "user_id"):
                                    search_for_user_id = self.get_valid_input("What user ID do you look for? [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False)
                                    if search_for_user_id == "BREAK":
                                        continue
                                    self.print_output_row_by_row(self.db.search_users_by_id(search_for_user_id, order_by=order_field, direction=direction))
                                    
                                elif search_by_what_at_users in ("2", "current balance"):
                                    balance = self.get_valid_input("What balance are you looking for? [Type 'break' or press Enter to cancel]", input_type="int")
                                    if balance == "BREAK":
                                        continue
                                    self.print_output_row_by_row(self.db.search_users_by_balance(balance, order_by=order_field, direction=direction))
                                    
                                elif search_by_what_at_users in ("3", "conditions"):
                                    self.print_warning("Leave blank (Press Enter) if you don't want to filter by that condition. Type 'break' to cancel.")
                                    
                                    u_id = self.get_valid_input("Filter by user_id keyword (Enter to skip):", input_type="str", allow_empty=True)
                                    if u_id == "BREAK":
                                        continue
                                    
                                    min_bal_str = self.get_valid_input("Filter by minimum current_balance (Enter to skip):", input_type="str", allow_empty=True)
                                    if min_bal_str == "BREAK":
                                        continue
                                        
                                    max_bal_str = self.get_valid_input("Filter by maximum current_balance (Enter to skip):", input_type="str", allow_empty=True)
                                    if max_bal_str == "BREAK":
                                        continue
                                    
                                    u_id_param = u_id if u_id else None
                                    min_bal_param = int(min_bal_str) if min_bal_str else None
                                    max_bal_param = int(max_bal_str) if max_bal_str else None
                                            
                                    results = self.db.search_users_with_conditions(
                                        user_id=u_id_param, 
                                        min_balance=min_bal_param, 
                                        max_balance=max_bal_param,
                                        order_by=order_field,
                                        direction=direction
                                    )
                                    self.print_output_row_by_row(results)
                            else:
                                self.print_error(f"Incorrect value! ({search_by_what_at_users})")
                                continue
                                
                        elif search_type == "ledger":
                            search_by_what_at_ledger = self.get_valid_input("What do you want to search by? \n 1 => user_id \n 2 => points \n 3 => reason \n 4 => conditions \n [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False).lower()
                            if search_by_what_at_ledger == "BREAK":
                                continue
                                
                            if self.check_search_by_what_at_ledger(search_by_what_at_ledger):
                                if search_by_what_at_ledger in ("1", "user_id"):
                                    user_id = self.get_valid_input("What user ID do you look for? [Type 'break' or press Enter to cancel]", input_type="str", allow_empty=False)
                                    if user_id == "BREAK":
                                        continue
                                    self.print_output_row_by_row(self.db.search_ledger_by_user_id(user_id, order_by=order_field, direction=direction))
                                    
                                elif search_by_what_at_ledger in ("2", "points"):
                                    points = self.get_valid_input("What points do you look for? [Type 'break' or press Enter to cancel]", input_type="int")
                                    if points == "BREAK":
                                        continue
                                    self.print_output_row_by_row(self.db.search_ledger_by_point(points, order_by=order_field, direction=direction))
                                    
                                elif search_by_what_at_ledger in ("3", "reason"):
                                    keywords = []
                                    self.print_warning("Type keywords one by one. Press Enter on empty line to finish, or type 'break' to cancel.")
                                    while True:
                                        kw = self.get_valid_input("Add a keyword (Enter to finish):", input_type="str", allow_empty=True)
                                        if kw == "BREAK":
                                            keywords = []
                                            break
                                        if kw is None or kw == "":
                                            break
                                        keywords.append(kw)
                                    if keywords:
                                        self.print_output_row_by_row(self.db.search_ledger_by_keywords(keywords, order_by=order_field, direction=direction))
                                        
                                elif search_by_what_at_ledger in ("4", "conditions"):
                                    self.print_warning("Leave blank (Press Enter) if you don't want to filter by that condition. Type 'break' to cancel.")
                                    
                                    u_id = self.get_valid_input("Filter by user_id keyword (Enter to skip):", input_type="str", allow_empty=True)
                                    if u_id == "BREAK":
                                        continue
                                        
                                    min_p_str = self.get_valid_input("Filter by minimum points (Enter to skip):", input_type="str", allow_empty=True)
                                    if min_p_str == "BREAK":
                                        continue
                                        
                                    max_p_str = self.get_valid_input("Filter by maximum points (Enter to skip):", input_type="str", allow_empty=True)
                                    if max_p_str == "BREAK":
                                        continue
                                        
                                    u_id_param = u_id if u_id else None
                                    min_p_param = int(min_p_str) if min_p_str else None
                                    max_p_param = int(max_p_str) if max_p_str else None
                                            
                                    keywords = []
                                    add_kw = self.get_valid_input("Do you want to filter by reason keywords? (y/n)", input_type="str", allow_empty=False).lower()
                                    if add_kw == "y":
                                        while True:
                                            kw = self.get_valid_input("Add a keyword (Enter to finish):", input_type="str", allow_empty=True)
                                            if kw is None or kw == "":
                                                break
                                            keywords.append(kw)
                                            
                                    results = self.db.search_ledger_with_conditions(
                                        user_id=u_id_param, 
                                        min_points=min_p_param, 
                                        max_points=max_p_param, 
                                        keywords=keywords if keywords else None,
                                        order_by=order_field,
                                        direction=direction
                                    )
                                    self.print_output_row_by_row(results)
                    else:
                        self.print_error(f"incorrect value! ({search_type})")
                        continue
                elif cmd == "exit":
                    break
                else:
                    self.print_error("Unavailable command!")
        except Exception as e:
            self.print_error(error=e)