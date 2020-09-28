import psycopg2
from psycopg2 import extras
from config import *


class CategoryBrowser:

    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

    def categories_browser(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT category_id, category.name AS category_name, COUNT(*) AS nb_products "
                       "FROM product_category LEFT JOIN category ON product_category.category_id = category.id "
                       "GROUP BY category_id, category.name ORDER BY nb_products DESC LIMIT 30")
        query_result = cursor.fetchall()
        cursor.close()

        page_size = 10
        page = 0
        cat_options = query_result[(page * page_size):(page * page_size) + page_size]
        for index, value in enumerate(cat_options):
            print(index, value)
        while True:
            try:
                category_choice = int(input("Please choose a category : "))
            except ValueError:
                print("Please choose one of the shown numbers")
                continue
            else:
                break
        print("You have chosen : ", cat_options[category_choice][1])
        user_choice = (cat_options[category_choice][0])

        return user_choice

    def product_browser(self, category_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT product.name AS product_name, nutrition_grade, id FROM product "
                       "INNER JOIN product_category ON "
                       "product.id = product_category.product_id WHERE category_id = %s", [category_id])
        product_result = cursor.fetchall()
        cursor.close()
        page_size = 10
        page = 0
        prod_options = product_result[(page * page_size):(page * page_size) + page_size]
        for index, value in enumerate(prod_options):
            print(index, value)

        while True:
            try:
                product_choice = int(input("Please choose your product: "))
            except ValueError:
                print("Please choose one of the shown numbers")
                continue
            else:
                break
        print("You have chosen : ", prod_options[product_choice][0])
        product = prod_options[product_choice]

        return {"id": product[2], "name": product[0], "nutrition_grade": product[1]}
