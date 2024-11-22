import logging
import sqlite3

from app.db import get_db_connection


class Products:
    def get_all_products(self):
        query = "SELECT * FROM products"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                products = cursor.fetchall()

                return products
        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return None

    def get_product_by_id(self, product_id):
        query = "SELECT * FROM products WHERE id = ?"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (product_id,))
                product = cursor.fetchone()

                return product
        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return None

    def add_product(self, product_name, price, stock):
        query = "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (product_name, price, stock))
                conn.commit()

                return True
        except sqlite3.IntegrityError as f:
            logging.error(f"Error: {f}")
            return False

        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return False

    def edit_product(self, product_id, product_name, price, stock):
        query = "UPDATE products SET name = ?, price = ?, stock = ? WHERE id = ?"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (product_name, price, stock, product_id))
                conn.commit()

                return True
        except sqlite3.IntegrityError as f:
            logging.error(f"Error: {f}")
            return False

        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return False

    def delete_product(self, product_id):
        query = "DELETE FROM products WHERE id = ?"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (product_id,))
                conn.commit()

                return True
        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return False
