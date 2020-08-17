import psycopg2
from psycopg2 import extras
from config import *
import off_class as cl
from Categories_Browser import *

conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

new_data = 0
products_list = []
categories_list = []


class Substitutes:

    def get_substitutes(self, product):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s_products = []
        if product.nutrition_grade == "d" or product.nutrition_grade == "e":
            cur.execute("""SELECT * FROM product WHERE category LIKE %s AND nutrition_grade='a' 
                            OR category LIKE %s AND nutrition_grade='b'
                            OR category LIKE %s AND nutrition_grade='b' """,
                        (product.category, product.category, product.category))
            result = cur.fetchall()
            for element in result:
                s_products.append(
                    cl.Product(element['name'], element['store'], element['nutrition_grade'], element['url'],
                               element['category']))
            return s_products

        else:
            cur.execute("""SELECT * FROM product WHERE category LIKE %s AND nutrition_grade='a' """,
                        tuple(product.category))
            result = cur.fetchall()
            for element in result:
                s_products.append(
                    cl.Product(element['name'], element['store'], element['nutrition_grade'], element['url'],
                               element['category']))
            return s_products

    def substitutes_browser(self, product):
        substitutes = self.get_substitutes(product)
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
                self.print_product(substitutes[int(uinput) - 1])
                continue
            if uinput == '>':
                page_min += 10
                page_max += 10
            if uinput == '<' and page_min > 0:
                page_min -= 10
                page_max -= 10
