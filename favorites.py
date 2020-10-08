import psycopg2
from psycopg2 import extras
from config import *


class Favorites:
    """
    Enables the user to see all his favorite products that were saved into the Database
    """

    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

    def get_products_from_favorite(self):
        """
        Shows all of the saved favorite substitutes of the user
        :return: A list of all the saved substitutes with their name, nutrition grade, where to buy and the URL for
                 more information on the product
        """
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM favorite LEFT JOIN product ON favorite.replacement_product_id = product.id")
        query_result = cursor.fetchall()
        cursor.close()
        favorite_db_products = []
        for element, index, id, name, store, nutri, url in query_result:
            print(f"Nom : {name} \n Magasin : {store} \n Grade nutritionnel : {nutri} \n URL : {url} \n")
        return favorite_db_products
