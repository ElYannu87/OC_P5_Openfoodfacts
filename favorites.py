import psycopg2
from psycopg2 import extras
from config import *


class Favorites:

    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

    def get_products_from_favorite(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM favorite LEFT JOIN product ON favorite.replacement_product_id = product.id")
        query_result = cursor.fetchall()
        cursor.close()
        favorite_db_products = []
        for element, index, id, name, store, nutri, url in query_result:
            print(element, index, id, name, store, nutri, url)
        return favorite_db_products

    def favorite_browser(self):
        pass
