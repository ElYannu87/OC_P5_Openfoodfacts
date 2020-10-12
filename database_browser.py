from typing import List, Tuple

import psycopg2
from psycopg2 import extras
from config import *
from menu import Menu


class DatabaseBrowser:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DatabaseBrowser()
        return cls._instance

    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

    def get_categories(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT category_id, category.name AS category_name, COUNT(*) AS nb_products "
                       "FROM product_category LEFT JOIN category ON product_category.category_id = category.id "
                       "GROUP BY category_id, category.name ORDER BY nb_products DESC LIMIT 30")
        query_result = cursor.fetchall()  # type: List[Tuple[int, str, int]]
        cursor.close()
        return query_result

    def get_products(self, category_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT product.name AS product_name, nutrition_grade, id FROM product "
                       "INNER JOIN product_category ON "
                       "product.id = product_category.product_id WHERE category_id = %s", [category_id])
        product_result = cursor.fetchall()
        cursor.close()
        return product_result

    def get_substitutes(self, product_ng, category_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT nutrition_grade, name, id FROM product INNER JOIN product_category ON "
                       "product.id = product_category.product_id WHERE category_id = %s AND product.name "
                       "IS NOT NULL AND product.nutrition_grade < %s ORDER BY product.nutrition_grade",
                       (category_id, product_ng))
        substitute_result = cursor.fetchall()
        cursor.close()
        return substitute_result
