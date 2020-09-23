import psycopg2
from psycopg2 import extras
from config import *


class SubstitutesFinder:

    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

    def get_substitutes(self, product_ng, category_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT nutrition_grade, name FROM product INNER JOIN product_category ON "
                       "product.id = product_category.product_id WHERE category_id = %s AND product.name "
                       "IS NOT NULL AND product.nutrition_grade < %s ORDER BY product.nutrition_grade",
                       (category_id, product_ng))
        substitute_result = cursor.fetchall()
        cursor.close()

        page_size = 10
        page = 0
        substitutes = substitute_result[(page * page_size):(page * page_size) + page_size]
        for index, value in enumerate(substitutes):
            print(index, value)

        substitutes_choice = int(input("Please choose your substitute: "))
        print("You have chosen : ", substitutes[substitutes_choice])
        user_substitute_choice = (substitutes[substitutes_choice])

        return user_substitute_choice
