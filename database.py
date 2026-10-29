from typing import Literal, Optional, List, Any
import sqlite3

class FETDatabase:
    def __init__(self, db_name: str = 'FET.db'):
        self.db_name = db_name
        self.setup_tables()

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        return conn, conn.cursor()

    def setup_tables(self):
        conn, cursor = self.get_connection()
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
        conn.commit()
        conn.close()

    def add_user(self, user_id: str):
        conn, cursor = self.get_connection()
        cursor.execute("INSERT INTO users (user_id, current_balance) values (?, 0)", (user_id,))
        conn.commit()
        conn.close()
        return True

    def add_points(self, user_id: str, points: int, reason: str):
        conn, cursor = self.get_connection()
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
        conn.close()
        return True

    def check_user(self, user_id: str):
        conn, cursor = self.get_connection()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def get_table_data(self, table: str, order_by: str = "default", direction: str = "ASC"):
        conn, cursor = self.get_connection()
        valid_dir = "DESC" if direction.upper() == "DESC" else "ASC"
        
        if table == "users":
            col = "current_balance" if order_by in ("balance", "current_balance", "points") else "user_id"
        elif table == "ledger":
            col = "points" if order_by in ("points", "balance") else "x_id"
        else:
            col = "user_id"

        cursor.execute(f"SELECT * FROM {table} ORDER BY {col} {valid_dir}")
        result = cursor.fetchall()
        conn.close()
        return result

    def search_users_by_id(self, user_id: str, order_by: str = "user_id", direction: str = "ASC"):
        conn, cursor = self.get_connection()
        valid_dir = "DESC" if direction.upper() == "DESC" else "ASC"
        col = "current_balance" if order_by in ("balance", "current_balance", "points") else "user_id"
        
        cursor.execute(f"SELECT * FROM users WHERE user_id LIKE ? ORDER BY {col} {valid_dir}", (f"%{user_id}%",))
        result = cursor.fetchall()
        conn.close()
        return result

    def search_users_by_balance(self, balance: int, order_by: str = "user_id", direction: str = "ASC"):
        conn, cursor = self.get_connection()
        valid_dir = "DESC" if direction.upper() == "DESC" else "ASC"
        col = "current_balance" if order_by in ("balance", "current_balance", "points") else "user_id"
        
        cursor.execute(f"SELECT * FROM users WHERE current_balance = ? ORDER BY {col} {valid_dir}", (balance,))
        result = cursor.fetchall()
        conn.close()
        return result

    def search_ledger_by_keywords(self, keywords: List[str], order_by: str = "x_id", direction: str = "ASC"):
        if not keywords:
            return []
        conn, cursor = self.get_connection()
        valid_dir = "DESC" if direction.upper() == "DESC" else "ASC"
        col = "points" if order_by in ("points", "balance") else "x_id"

        clauses = []
        params = []
        for kw in keywords:
            clauses.append("reason LIKE ?")
            params.append(f"%{kw}%")
        
        sql_query = f"SELECT * FROM ledger WHERE {' OR '.join(clauses)} ORDER BY {col} {valid_dir}"
        cursor.execute(sql_query, tuple(params))
        result = cursor.fetchall()
        conn.close()
        return result

    def search_ledger_by_user_id(self, user_id: str, order_by: str = "x_id", direction: str = "ASC"):
        conn, cursor = self.get_connection()
        valid_dir = "DESC" if direction.upper() == "DESC" else "ASC"
        col = "points" if order_by in ("points", "balance") else "x_id"
        
        cursor.execute(f"SELECT * FROM ledger WHERE user_id LIKE ? ORDER BY {col} {valid_dir}", (f"%{user_id}%",))
        result = cursor.fetchall()
        conn.close()
        return result

    def search_ledger_by_point(self, point: int, order_by: str = "x_id", direction: str = "ASC"):
        conn, cursor = self.get_connection()
        valid_dir = "DESC" if direction.upper() == "DESC" else "ASC"
        col = "points" if order_by in ("points", "balance") else "x_id"
        
        cursor.execute(f"SELECT * FROM ledger WHERE points = ? ORDER BY {col} {valid_dir}", (point,))
        result = cursor.fetchall()
        conn.close()
        return result

    def search_users_with_conditions(self, user_id=None, min_balance=None, max_balance=None, order_by="user_id", direction="ASC"):
        conn, cursor = self.get_connection()
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
        cursor.execute(sql_query, tuple(params))
        result = cursor.fetchall()
        conn.close()
        return result

    def search_ledger_with_conditions(self, user_id=None, min_points=None, max_points=None, keywords=None, order_by="x_id", direction="ASC"):
        conn, cursor = self.get_connection()
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
        cursor.execute(sql_query, tuple(params))
        result = cursor.fetchall()
        conn.close()
        return result