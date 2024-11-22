import logging
import sqlite3

from app.db import get_db_connection


class Customers:
    def get_all_customers(self):
        query = "SELECT * FROM customers"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                customers = cursor.fetchall()

                return customers
        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return None

    def get_customer_by_id(self, customer_id):
        query = "SELECT * FROM customers WHERE id = ?"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (customer_id,))
                customer = cursor.fetchone()

                return customer
        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return None

    def add_customer(self, customer_name):
        query = "INSERT INTO customers (name) VALUES (?)"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (customer_name,))
                conn.commit()

                return True
        except sqlite3.IntegrityError as f:
            logging.error(f"Error: {f}")
            return False

        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return False

    def edit_customer(self, customer_id, customer_name):
        query = "UPDATE customers SET name = ? WHERE id = ?"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (customer_name, customer_id))
                conn.commit()

                return True
        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return False

    def delete_customer(self, customer_id):
        query = "DELETE FROM customers WHERE id = ?"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (customer_id,))
                conn.commit()

                return True
        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return False
