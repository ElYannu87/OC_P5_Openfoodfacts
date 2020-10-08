import psycopg2
from psycopg2 import extras
from config import *


class SaveProducts:
    """
    Saves the substitute products
    """

    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

    def save_user_product(self, product, sub):
        """
        Saves the chosen product and the substitute into the favorite table in the Database
        ---------------------------------
        :param product: The initially chosen product
        :param sub: the chosen substitute
        """
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("INSERT INTO favorite(source_product_id, replacement_product_id)  VALUES (%s, %s)",
                       (product, sub))
        self.conn.commit()
        cursor.close()
