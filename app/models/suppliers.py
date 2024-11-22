import logging
import sqlite3

from app.db import get_db_connection


class Suppliers:
    def get_all_suppliers(self):
        query = "SELECT * FROM suppliers"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                suppliers = cursor.fetchall()

                return suppliers
        except sqlite3.DatabaseError as e:
            logging.error("Database error: %s", e)
            return None

    def get_supplier_by_id(self, supplier_id):
        query = "SELECT * FROM suppliers WHERE id = ?"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (supplier_id,))
                supplier = cursor.fetchone()

                return supplier
        except sqlite3.DatabaseError as e:
            logging.error("Database error: %s", e)
            return None

    def add_supplier(self, company_name, supplier_name, email, phone):
        query = "INSERT INTO suppliers (company_name, supplier_name, email, phone) VALUES (?, ?, ?, ?)"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (company_name, supplier_name, email, phone))
                conn.commit()

                return True
        except sqlite3.IntegrityError as f:
            logging.error("Integrity error: %s", f)
            return False

        except sqlite3.DatabaseError as e:
            logging.error("Database error: %s", e)
            return False

    def edit_supplier(self, supplier_id, company_name, supplier_name, email, phone):
        query = "UPDATE suppliers SET company_name = ?, supplier_name = ?, email = ?, phone = ? WHERE id = ?"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    query, (company_name, supplier_name, email, phone, supplier_id)
                )
                conn.commit()

                return True
        except sqlite3.IntegrityError as f:
            logging.error("Integrity error: %s", f)
            return False

        except sqlite3.DatabaseError as e:
            logging.error("Database error: %s", e)
            return False

    def delete_supplier(self, supplier_id):
        query = "DELETE FROM suppliers WHERE id = ?"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (supplier_id,))
                conn.commit()

                return True
        except sqlite3.DatabaseError as e:
            logging.error("Database error: %s", e)
            return False
