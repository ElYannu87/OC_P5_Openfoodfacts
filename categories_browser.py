import psycopg2
from psycopg2 import extras
from config import *


class CategoryBrowser:

    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)
        self.categories_browser()

    def categories_browser(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT category_id, category.name as category_name, COUNT(*) as nb_products "
                       "FROM product_category LEFT JOIN category ON product_category.category_id = category.id "
                       "GROUP BY category_id, category.name ORDER BY nb_products DESC LIMIT 30")
        query_result = cursor.fetchall()

        page_size = 10
        page = 0
        cat_options = query_result[(page * page_size):(page * page_size) + page_size]
        for index, value in enumerate(cat_options):
            print(index, value)

        category_choice = int(input("Please choose a category : "))
        print("You have chosen : ", cat_options[category_choice][1])
        user_choice = (cat_options[category_choice][0])

        cursor.execute("SELECT product.name as product_name, nutrition_grade, id FROM product "
                       "INNER JOIN product_category ON "
                       "product.id = product_category.product_id WHERE category_id = %s", [user_choice])
        product_result = cursor.fetchall()
        page_size = 10
        page = 0
        prod_options = product_result[(page * page_size):(page * page_size) + page_size]
        for index, value in enumerate(prod_options):
            print(index, value)
        product_choice = int(input("Please choose your product: "))
        print("You have chosen : ", prod_options[product_choice][0])
        user_prod_choice = (prod_options[product_choice][2])
        print(user_prod_choice)
