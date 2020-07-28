import psycopg2
from psycopg2 import extras
import requests

import off_class as cl

conn = psycopg2.connect("dbname=OC_Project_5 user=user password=Rg15271528ibaneZ host=localhost port=5432")

products_list = []


def fill_product():
    page = 1
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    for page in range(1, 30):
        result = requests.get(
            'https://fr.openfoodfacts.org/cgi/search.pl?page_size=1000&page={}&action=process&json=1'.format(
                page)).json()
        for element in result['products']:
            try:
                product_info = (
                    element["product_name"], element["stores"], element["nutrition_grade_fr"], element["url"],
                    element['categories_tags'][0])
                products_list.append(
                    cl.Product(element["product_name"], element["stores"], element["nutrition_grade_fr"],
                               element["url"], element['categories_tags'][0]))
                cur.execute("INSERT INTO product" "(name, store, nutrition_grade, url, category)""VALUES (%s, %s, "
                            "%s, %s, %s)", product_info)
                conn.commit()
                print(len(products_list), " products")
            except KeyError:  # Don't take lines without 'product_name'
                pass
            except conn.OperationalError:  # Don't take the products with encoding error
                pass
            except conn.DataError:  # Pass when product name is too long
                pass


fill_product()
