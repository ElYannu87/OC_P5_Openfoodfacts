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


def fill_category():
    cursor = conn.cursor()
    result = requests.get('https://fr.openfoodfacts.org/categories.json').json()
    for element in result['tags']:
        if element['products'] > 1500:
            try:
                categories_list.append(cl.Category(element["id"], element["name"], element["url"]))
                cursor.execute("INSERT INTO category (tag, name, url) VALUES  (%s, %s, %s)",
                               (element["id"], element["name"], element["url"]))
                print(len(categories_list), "categories")
            except conn.OperationalError:  # Don't take the products with encoding error
                pass
            except conn.DataError:  # Pass when product name is too long
                pass
        conn.commit()


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
        if len(categories_list) - page_max < 10 <= page_max:
            page_max += len(categories_list) - page_max
            if page_max < 10:
                page_min = 0
            else:
                page_min = page_max - 10
        if page_min < 0:
            page_min = 0
            page_max = 10

        for i in range(page_min, page_max):
            print("{} -{}".format(i + 1, categories_list[i].name))

        uinput = input(
            "Entrez : Numéro pour sélectionner la catégorie""| > page suivante | < page précédente " "| 0 - revenir "
            "au menu principal\n")

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
    global products_list
    global categories_list

    category_products = select_products_from_category(category_name)
    page_min = 0
    page_max = 10
    while True:
        if len(category_products) - page_max < 10 <= page_max:
            page_max += len(category_products) - page_max
            if page_max < 10:
                page_min = 0
            else:
                page_min = page_max - 10
            if page_min < 0:
                page_min = 10
                page_max = 10

            if len(category_products) == 0:
                print("\n Il n'y a pas de produits dans cette catégorie")
                break

            print("\n Affichage des produits de la catégorie {}".format(categories_list[c_id].name, ))
            for i in range(page_min, page_max):
                print("{} - {}".format(i + 1, category_products[i].name))

            uinput = input(
                "Entrez : Numéro pour sélectionner un produit""| > page suivante | < page précédente " "| 0 - revenir "
                "au menu principal\n")

            if uinput == "0":
                break
            if uinput == ">":
                page_max += 10
                page_min += 10
            if uinput == "<":
                page_max -= 10
                page_min -= 10
            if uinput.isdigit():
                if 0 < int(uinput) <= len(category_products):
                    print_product(category_products[int(uinput) - 1])


def select_products_from_category(category):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT * FROM product WHERE category LIKE %s """, tuple(category))
    result = cur.fetchall()
    category_products = []
    for element in result:
        category_products.append(
            cl.Product(element['name'], element['store'], element['nutrition_grade'], element['url'],
                       element['category']))
    return category_products


def print_product(product):
    while True:
        print("\n\t__Fiche du Produit__\n")
        print("Nom du produit : " + product.name)
        print("Magasin : " + product.store)
        print("Nutri score: " + product.nutrition_grade)
        print("URL : " + product.url)

        uinput = input("Entrez: 1 - Recherche d'un produit plus sain | 2 - Enregistrer | 3 - Supprimer le produit "
                       "des favoris| 0 - Revenir aux produits ")

        if uinput == '0':
            break

        if uinput == '1':
            substitutes_browser(product)

        if uinput == '2':
            save_user_product(product)

        if uinput == '3':
            drop_user_product(product)


def drop_user_product(product):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "DELETE FROM favorite WHERE name = '%s' "
    cur.execute(sql % product.name)
    cur.close()
    conn.commit()
    print("\nProduit supprimé de votre liste.")


def save_user_product(product):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM favorite")
    result = cur.fetchall()
    exist = 0
    for element in result:
        if element['name'] == product.name:
            exist = 1
    if exist == 1:
        print("Produit déjà enregistré.")
    else:
        cur.execute('INSERT INTO favorite (name, store, nutrition_grade, url, category)'
                    ' VALUES (%s, %s, %s, %s, %s)',
                    (product.name, product.store, product.nutrition_grade, product.url, product.category))
        print("\nProduit sauvegardé.")
    cur.close()
    conn.commit()


def get_substitutes(product):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s_products = []
    if product.nutrition_grade == "d" or product.nutrition_grade == "e":
        cur.execute("""SELECT * FROM product WHERE category LIKE %s AND nutrition_grade='a' 
                        OR category LIKE %s AND nutrition_grade='b'
                        OR category LIKE %s AND nutrition_grade='b' """,
                    (product.category, product.category, product.category))
        result = cur.fetchall()
        for element in result:
            s_products.append(cl.Product(element['name'], element['store'], element['nutrition_grade'], element['url'],
                                         element['category']))
        return s_products

    else:
        cur.execute("""SELECT * FROM product WHERE category LIKE %s AND nutrition_grade='a' """, tuple(product.category))
        result = cur.fetchall()
        for element in result:
            s_products.append(cl.Product(element['name'], element['store'], element['nutrition_grade'], element['url'],
                                         element['category']))
        return s_products


def substitutes_browser(product):
    substitutes = get_substitutes(product)
    page_min = 0
    page_max = 10
    while True:
        if len(substitutes) - page_max < 10 <= page_max:
            page_max += len(substitutes) - page_max
            if page_max < 10:
                page_min = 0
            else:
                page_min = page_max - 10
        if page_min < 0:
            page_min = 0
            page_max = 10

        print("\nListe des {} substitution pour le produit \"{}\" : \n".format(len(substitutes), product.name))
        if len(substitutes) == 0:
            print("\nIl n'y a pas de substitut pour votre produit.\nRetour à la fiche produit.\n")
            break
        else:
            for i in range(page_min, page_max):
                print("{} - {}".format(i + 1, substitutes[i].name))

        uinput = input("\nEntrez: Numéro - selectionner un produit | > - page suivante |"
                       " < - page précedente | 0 - revenir au produit\n")

        if uinput == '0':
            break
        if uinput.isdigit():
            print_product(substitutes[int(uinput) - 1])
            continue
        if uinput == '>':
            page_min += 10
            page_max += 10
        if uinput == '<' and page_min > 0:
            page_min -= 10
            page_max -= 10


def favorite_browser():
    page_min = 0
    page_max = 10
    while True:
        favorite_products = get_products_from_favorite()
        if len(favorite_products) - page_max < 10 <= page_max:
            page_max = len(favorite_products)
            if page_max < 10:
                page_min = 0
            else:
                page_min = page_max - 10
        if page_min < 0:
            page_min = 0
            page_max = 10
        if len(favorite_products) < 10:
            page_max = len(favorite_products)
            page_min = 0

        print("\n__Liste des produits enregistrés__")
        for i in range(page_min, page_max):
            print("{} - {}".format(i + 1, favorite_products[i].name, ))
        uinput = input("\nEntrez: Numéro - selectionner un produit | > - page suivante |"
                       " < - page précedente | 0 - revenir au menu principal)\n")

        if uinput == '0':
            break

        if uinput == '>':
            page_max += 10
            page_min += 10

        if uinput == '<' and page_min > 0:
            page_max -= 10
            page_min -= 10

        if uinput.isdigit():
            if 0 < int(uinput) <= len(favorite_products):
                print_product(favorite_products[int(uinput) - 1])


def get_products_from_favorite():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM favorite")
    result = cur.fetchall()
    cur.close()
    favorite_db_products = []
    for element in result:
        favorite_db_products.append(
            cl.Product(element['name'], element['store'], element['nutrition_grade'], element['url'],
                       element['category']))
    return favorite_db_products


def client_menu():
    global products_list
    global categories_list

    running = True

    if new_data == 1:
        fill_product()
        fill_category()

    else:
        print("searching for data...")
        products_list = get_products_from_db()
        categories_list = get_categories_from_db()

    while running is True:
        print("""
===================================
     Bienvenue à openfoodfacts!
===================================
1. Quel aliment souhaitez-vous remplacer ?
2. Afficher la liste des favoris
3. QUITTER
        """)
        uinput = input("Entrez: Un numéro pour choisir un menu")

        if uinput == '1':
            categories_browser()
            continue

        if uinput == '2':
            favorite_browser()
            continue

        if uinput == '3':
            running = False


client_menu()
