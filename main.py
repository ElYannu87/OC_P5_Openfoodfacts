import psycopg2
from psycopg2 import extras
import requests
from config import *
import off_class as cl

conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

new_data = 0
products_list = []
categories_list = []


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


def fill_category():
    cursor = conn.cursor()
    result = requests.get('https://fr.openfoodfacts.org/categories.json').json()
    for element in result['tags']:
        if element['products'] > 1500:
            try:
                categories_list.append(cl.Category(element["id"], element["name"], element["url"]))
                cursor.execute("INSERT INTO category (tag, name, url)" "VALUES  (%s, %s, %s)",
                               (element["id"], element["name"], element["url"]))
                conn.commit()
                print(len(categories_list), "categories")
            except conn.OperationalError:  # Don't take the products with encoding error
                pass
            except conn.DataError:  # Pass when product name is too long
                pass


def get_products_from_db():
    """Get a list of products from the database"""
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM product")
    result = cur.fetchall()
    cur.close()

    db_products = []
    for element in result:
        db_products.append(cl.Product(element['name'], element['store'], element['nutrition_grade'], element['url'],
                                      element['category']))
        return db_products


def get_categories_from_db():
    """Get a list of categories from the database"""
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM category")
    result = cur.fetchall()
    cur.close()

    db_categories = []
    for element in result:
        db_categories.append(cl.Category(element['tag'], element['name'], element['url']))
        return db_categories


fill_category()
