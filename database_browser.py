from typing import List, Tuple

import psycopg2
from psycopg2 import extras
from config import *


class DatabaseBrowser:
    '''
    Class that is called to execute the different SQL querys to the Database
    Each function will send a specific command to the Database to retrieve or save informations.
    '''
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DatabaseBrowser()
        return cls._instance

    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

    def get_categories(self):
        '''
        :returns : the 30 most popular categories
        '''
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT category_id, category.name AS category_name, COUNT(*) AS nb_products "
                       "FROM product_category LEFT JOIN category ON product_category.category_id = category.id "
                       "GROUP BY category_id, category.name ORDER BY nb_products DESC LIMIT 30")
        query_result = cursor.fetchall()  # type: List[Tuple[int, str, int]]
        cursor.close()
        return query_result

    def get_products(self, category_id):
        '''
        ;:param : category_id chosen by user
        :returns : The products chosen by user
        '''
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT product.name AS product_name, nutrition_grade, id FROM product "
                       "INNER JOIN product_category ON "
                       "product.id = product_category.product_id WHERE category_id = %s", [category_id])
        product_result = cursor.fetchall()
        cursor.close()
        return product_result

    def get_substitutes(self, product_ng, category_id):
        """
        Compares the product chosen by the user to find a better alternative by comparing the nutrition grade
        ---------------------------------
        :param product_ng: nutrition grade
        :param category_id: category id
        :return: all products in the same category with a better nutrition grade
        """
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT nutrition_grade, name, id FROM product INNER JOIN product_category ON "
                       "product.id = product_category.product_id WHERE category_id = %s AND product.name "
                       "IS NOT NULL AND product.nutrition_grade < %s ORDER BY product.nutrition_grade",
                       (category_id, product_ng))
        substitute_result = cursor.fetchall()
        cursor.close()
        return substitute_result

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
        return query_result
