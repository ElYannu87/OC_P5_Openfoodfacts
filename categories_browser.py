import psycopg2
from psycopg2 import extras
from config import *
import off_class as cl



conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

new_data = 0
products_list = []
categories_list = []


class CategorieBrowser:

    def categories_browser(self):
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
                self.categories_product_browser(int(uinput)-1, categories_list[int(uinput)-1].tag)


    def categories_product_browser(self, c_id, category_name):
        global products_list
        global categories_list

        category_products = self.select_products_from_category(category_name)
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
                        self.print_product(category_products[int(uinput) - 1])


    def select_products_from_category(self, category):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""SELECT * FROM product WHERE category LIKE %s """, tuple(category))
        result = cur.fetchall()
        category_products = []
        for element in result:
            category_products.append(
                cl.Product(element['name'], element['store'], element['nutrition_grade'], element['url'],
                           element['category']))
        return category_products


    def print_product(self, product):
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
                self.substitutes_browser(product)

            if uinput == '2':
                self.save_user_product(product)

            if uinput == '3':
                self.drop_user_product(product)
