import logging
import sqlite3

from app.db import get_db_connection


class Sales:
    def get_all_sales(self):
        query = "SELECT * FROM sales ORDER BY product_sold DESC"

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                sales = cursor.fetchall()

                return sales
        except sqlite3.DatabaseError as e:
            logging.error(f"Error: {e}")
            return None
