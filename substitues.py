import psycopg2
from psycopg2 import extras
from config import *
from menu import Menu


class SubstitutesFinder:
    """
    Proposes the substitutes for the the product chosen by the user
    """

    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

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

        menu_elements = list()
        for e in substitute_result:
            menu_elements.append((e[2], f"{e[1]} : {e[0]}"))
        menu = Menu("Liste des produits", "choisissez un substitue: ", menu_elements)
        substitutes_choice = menu.result
        database_product = substitute_result
        i = 0
        while substitutes_choice[0] != database_product[i][2]:
            i = i + 1

        return substitutes_choice
