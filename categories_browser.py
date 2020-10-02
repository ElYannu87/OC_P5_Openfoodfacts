from typing import Tuple, List

import psycopg2
from psycopg2 import extras
from config import *
from menu import Menu


class CategoryBrowser:

    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

    def categories_browser(self) -> Tuple[int, str]:
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT category_id, category.name AS category_name, COUNT(*) AS nb_products "
                       "FROM product_category LEFT JOIN category ON product_category.category_id = category.id "
                       "GROUP BY category_id, category.name ORDER BY nb_products DESC LIMIT 30")
        query_result = cursor.fetchall()  # type: List[Tuple[int, str, int]]
        cursor.close()
        menu_elements = list()  # type: List[Tuple[int, str]]
        for e in query_result:
            menu_elements.append((e[0], e[1]))
        menu = Menu("Liste des categories", "choisissez une catégorie: ", menu_elements)
        print(menu.result)
        category_chosen = menu.result  # type: Tuple[int, str]

        return category_chosen

    def product_browser(self, category_id: int):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT product.name AS product_name, nutrition_grade, id FROM product "
                       "INNER JOIN product_category ON "
                       "product.id = product_category.product_id WHERE category_id = %s", [category_id])
        product_result = cursor.fetchall()
        cursor.close()
        menu_elements = list()
        for e in product_result:
            menu_elements.append((e[2], f"{e[0]} : {e[1]}"))
        menu = Menu("Liste des produits", "choisissez un produit: ", menu_elements)
        print(menu.result)
        selected_product = menu.result
        print (selected_product)
        database_product = product_result
        i = 0
        while selected_product[0] != database_product[i][2]:
            i = i + 1
        print(selected_product)

        return {"id": database_product[i][2], "name": database_product[i][0], "nutrition_grade": database_product[i][1]}


