import psycopg2
from psycopg2 import extras
from config import *
import off_class as cl

conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

new_data = 0
products_list = []
categories_list = []


class Favorites:

    def favorite_browser(self):
        page_min = 0
        page_max = 10
        while True:
            favorite_products = self.get_products_from_favorite()
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
                    self.print_product(favorite_products[int(uinput) - 1])

    def get_products_from_favorite(self):
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
