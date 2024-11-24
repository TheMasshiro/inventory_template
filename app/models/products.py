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

    def add_product(self, product_name, price, stock, supplier_name):
        query = "INSERT INTO products (product_name, price, stock, supplier_name) VALUES (?, ?, ?, ?)"
        sales_query = "INSERT INTO sales (product_id, product_sold) VALUES (?, ?)"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (product_name, price, stock, supplier_name))
                conn.commit()

                product_id = cursor.lastrowid
                cursor.execute(sales_query, (product_id, 0))
                conn.commit()

                return True
        except sqlite3.IntegrityError as f:
            logging.error(f"Error: {f}")
            return False

    def edit_product(self, product_id, product_name, price, stock, supplier_name):
        query = "UPDATE products SET product_name = ?, price = ?, stock = ?, supplier_name = ? WHERE product_id = ?"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    query, (product_name, price, stock, supplier_name, product_id)
                )
                conn.commit()

                return True
        except sqlite3.IntegrityError as f:
            logging.error(f"Error: {f}")
            return False

        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return False

    def delete_product(self, product_id):
        query = "DELETE FROM products WHERE product_id = ?"
        sales_query = "DELETE FROM sales WHERE product_id = ?"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (product_id,))
                conn.commit()

                cursor.execute(sales_query, (product_id,))
                conn.commit()

                return True
        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return False
