from typing import Literal, Optional, List, Any
import sqlite3

class FETDatabase:
    def __init__(self, db_name: str = 'FET.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_tables()

    def setup_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            current_balance INTEGER
            )
            """,
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ledger (
            x_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            points INTEGER,
            reason TEXT
            )
            """,
        )
        self.conn.commit()

    def add_user(self, user_id: str):
        self.cursor.execute("INSERT INTO users (user_id, current_balance) values (?, 0)", (user_id,))
        self.conn.commit()
        return True

    def add_points(self, user_id: str, points: int, reason: str):
        self.cursor.execute(
            """
            INSERT INTO ledger (user_id, points, reason) values (?, ?, ?)
            """,
            (user_id, points, reason),
        )
        self.cursor.execute(
            "UPDATE users SET current_balance = current_balance + ? WHERE user_id = ?", 
            (points, user_id),
        )
        self.conn.commit()
        return True

    def check_user(self, user_id: str):
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()

    def get_table_data(self, table: str, order_by: str = "default", direction: str = "ASC"):
        valid_dir = "DESC" if direction.upper() == "DESC" else "ASC"
        
        if table == "users":
            col = "current_balance" if order_by in ("balance", "current_balance", "points") else "user_id"
        elif table == "ledger":
            col = "points" if order_by in ("points", "balance") else "x_id"
        else:
            col = "user_id"

        self.cursor.execute(f"SELECT * FROM {table} ORDER BY {col} {valid_dir}")
        return self.cursor.fetchall()

    def search_users_by_id(self, user_id: str, order_by: str = "user_id", direction: str = "ASC"):
        valid_dir = "DESC" if direction.upper() == "DESC" else "ASC"
        col = "current_balance" if order_by in ("balance", "current_balance", "points") else "user_id"
        
        self.cursor.execute(f"SELECT * FROM users WHERE user_id LIKE ? ORDER BY {col} {valid_dir}", (f"%{user_id}%",))
        return self.cursor.fetchall()

    def search_users_by_balance(self, balance: int, order_by: str = "user_id", direction: str = "ASC"):
        valid_dir = "DESC" if direction.upper() == "DESC" else "ASC"
        col = "current_balance" if order_by in ("balance", "current_balance", "points") else "user_id"
        
        self.cursor.execute(f"SELECT * FROM users WHERE current_balance = ? ORDER BY {col} {valid_dir}", (balance,))
        return self.cursor.fetchall()

    def search_ledger_by_keywords(self, keywords: List[str], order_by: str = "x_id", direction: str = "ASC"):
        if not keywords:
            return []
        valid_dir = "DESC" if direction.upper() == "DESC" else "ASC"
        col = "points" if order_by in ("points", "balance") else "x_id"

        clauses = []
        params = []
        for kw in keywords:
            clauses.append("reason LIKE ?")
            params.append(f"%{kw}%")
        
        sql_query = f"SELECT * FROM ledger WHERE {' OR '.join(clauses)} ORDER BY {col} {valid_dir}"
        self.cursor.execute(sql_query, tuple(params))
        return self.cursor.fetchall()

    def search_ledger_by_user_id(self, user_id: str, order_by: str = "x_id", direction: str = "ASC"):
        valid_dir = "DESC" if direction.upper() == "DESC" else "ASC"
        col = "points" if order_by in ("points", "balance") else "x_id"
        
        self.cursor.execute(f"SELECT * FROM ledger WHERE user_id LIKE ? ORDER BY {col} {valid_dir}", (f"%{user_id}%",))
        return self.cursor.fetchall()

    def search_ledger_by_point(self, point: int, order_by: str = "x_id", direction: str = "ASC"):
        valid_dir = "DESC" if direction.upper() == "DESC" else "ASC"
        col = "points" if order_by in ("points", "balance") else "x_id"
        
        self.cursor.execute(f"SELECT * FROM ledger WHERE points = ? ORDER BY {col} {valid_dir}", (point,))
        return self.cursor.fetchall()

    def search_users_with_conditions(self, user_id=None, min_balance=None, max_balance=None, order_by="user_id", direction="ASC"):
        valid_dir = "DESC" if direction.upper() == "DESC" else "ASC"
        col = "current_balance" if order_by in ("balance", "current_balance", "points") else "user_id"

        sql_query = f"SELECT * FROM users WHERE 1=1"
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
            
        sql_query += f" ORDER BY {col} {valid_dir}"
        self.cursor.execute(sql_query, tuple(params))
        return self.cursor.fetchall()

    def search_ledger_with_conditions(self, user_id=None, min_points=None, max_points=None, keywords=None, order_by="x_id", direction="ASC"):
        valid_dir = "DESC" if direction.upper() == "DESC" else "ASC"
        col = "points" if order_by in ("points", "balance") else "x_id"

        sql_query = f"SELECT * FROM ledger WHERE 1=1"
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
            
        sql_query += f" ORDER BY {col} {valid_dir}"
        self.cursor.execute(sql_query, tuple(params))
        return self.cursor.fetchall()