import logging
import sqlite3

from app.db import get_db_connection


class Sales:
    def get_product_id(self, product_name):
        query = "SELECT product_id FROM products WHERE product_name = ?"
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (product_name,))
                product_id = cursor.fetchone()

                return product_id
        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return None

    def get_all_product_name(self):
        query = "SELECT product_name FROM products"
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                products = cursor.fetchall()

                return products
        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return None

    def get_all_sales(self):
        query = "SELECT sales.sale_id, products.product_name, sales.product_sold, products.supplier_name FROM sales JOIN products ON sales.product_id = products.product_id"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                sales = cursor.fetchall()

                return sales
        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return None

    def add_sales(self, product_id, product_sold):
        query = "INSERT INTO sales (product_id, product_sold) VALUES (?, ?)"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (product_id, product_sold))
                conn.commit()
        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return None

    def edit_sales(self, sales_id, product_sold):
        query = "UPDATE sales SET product_sold = ? WHERE sale_id = ?"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (product_sold, sales_id))
                conn.commit()
        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return None

    def delete_sales(self, sales_id):
        query = "DELETE FROM sales WHERE sale_id = ?"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (sales_id,))
                conn.commit()
        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return None
