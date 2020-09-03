import psycopg2
from psycopg2 import extras
import requests
from config import *
import off_class as cl

conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

new_data = 0
products_list = []
categories_list = []


class FillDb:

    def fill_product(self):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        for page in range(1, 30):
            result = requests.get(
                'https://fr.openfoodfacts.org/cgi/search.pl?page_size=1000&page={}&action=process&json=1'.format(
                    page)).json()
            categories = self.fill_category(result)
            for element in result['products']:
                try:
                    for category in element['categories_tags']:
                        cur.execute()
                    product_info = (
                        element["product_name"], element["stores"], element["nutrition_grade_fr"], element["url"],
                        categories[element['categories_tags'][0]])
                    products_list.append(
                        cl.Product(element["product_name"], element["stores"], element["nutrition_grade_fr"],
                                   element["url"], element['categories_tags'][0]))
                    cur.execute("INSERT INTO product (name, store, nutrition_grade, url, category) VALUES (%s, %s, "
                                "%s, %s, %s)", product_info)
                    print(len(products_list), " products")
                except KeyError:  # Don't take lines without 'product_name'
                    pass
                except conn.OperationalError:  # Don't take the products with encoding error
                    pass
                except conn.DataError:  # Pass when product name is too long
                    pass
            conn.commit()


    def fill_category(self, product_list):
        categories = dict()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        for product in product_list['products']:
            categories_list = product['categories_tags']
            for category_name in categories_list:
                if category_name not in categories:
                    category_ids = cur.execute("SELECT id FROM category WHERE category.name LIKE %s", (category_name,))
                    if category_ids is None or len(category_ids) == 0:
                        category_id = cur.execute("INSERT INTO category(name, tag, url) VALUES (%s, %s, %s) RETURNING id", (category_name,"", ""))
                    else:
                        category_id = category_ids[0]
                    categories.__setitem__(category_name, category_id)
        return categories
