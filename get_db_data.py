import psycopg2
from psycopg2 import extras
from config import *
import off_class as cl

conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

new_data = 0
products_list = []
categories_list = []


class GetDbData:

    def get_products_from_db(self):
        """Get a list of products from the database"""
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM product")
        result = cur.fetchall()
        cur.close()

        db_products = []
        for element in result:
            db_products.append(cl.Product(element['name'], element['store'], element['nutrition_grade'], element['url'],
                                          element['category']))
            return db_products

    def get_categories_from_db(self):
        """Get a list of categories from the database"""
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM category")
        result = cur.fetchall()
        cur.close()

        db_categories = []
        for element in result:
            db_categories.append(cl.Category(element['tag'], element['name'], element['url']))
            return db_categories
