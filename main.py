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


def categories_browser():
    global products_list
    global categories_list

    page_min = 0
    page_max = 10
    while True:
        print("Sélectionner une catégorie:")
        if len(categories_list)-page_max < 10 <= 10 page_max :
            page_max += len(categories_list)-page_max
            if page_max < 10:
                page_min = 0
            else :
                page_min = page_max -10
        if page_min < 0:
            page_min = 0
            page_max = 10

        for i in range(page_min, page_max):
            print ("{} -{}".format (i+1, categories_list[i].name))

        uinput = input("Entrez : Numéro pour sélectionner la catégorie""| > page suivante | < page précédente " "| 0 - revenir au menu principal\n")

        if uinput == "0":
            break
        if uinput == ">":
            page_max += 10
            page_min += 10
        if uinput == "<":
            page_max -= 10
            page_min -= 10
        if uinput.isdigit():
            categories_product_browser(int(uinput)-1, categories_list[int(uinput)-1].tag)

def categories_product_browser(c_id, category_name):
    global categories_list
    global products_list

    category_products = select_product_from_category(category_name)
    page_min = 0
    page_max = 10
    while True:
        if len(category_products)-page_max < 10 <= page_max:
            page_max += len(category_products) -page_max
            if page_max < 10:
                page_min = 0
            else:
                page_min = page_max-10
        if page_min < 0:
            page_min =0
            page_max = 10






