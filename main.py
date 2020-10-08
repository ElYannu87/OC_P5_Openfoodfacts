from categories_browser import CategoryBrowser
from substitues import SubstitutesFinder
from save_products import SaveProducts
from favorites import Favorites
from config import *
import psycopg2


class Main:

    def __init__(self):
        self.check_database()
        self.main_screen()

    def check_database(self):
        connection = None
        try:
            # In PostgreSQL, default username is 'postgres' and password is 'postgres'.
            # And also there is a default database exist named as 'postgres'.
            # Default host is 'localhost' or '127.0.0.1'
            # And default port is '54322'.
            connection = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)
            print('Database connected.')

        except:
            print('Database not connected.')

        if connection is not None:
            connection.autocommit = True

            cur = connection.cursor()

            cur.execute("SELECT name FROM category")

            list_database = cur.fetchall()

            database_name = input('Enter database name to check exist or not: ')

            if (database_name,) in list_database:
                print("'{}' Database already exist".format(database_name))
            else:
                print("'{}' Database not exist.".format(database_name))
            connection.close()
            print('Done')

    def main_screen(self):

        loop = 1
        while loop:
            try:
                choice = int(input(
                    "1 - Choisir des aliments à substituer. \n"
                    "2 - Voir mes favoris. \n"
                    "3 - Quitter le programme. \n"
                ))
                if choice == 1:
                    cb = CategoryBrowser()
                    category_id = cb.categories_browser()
                    product = cb.product_browser(category_id[0])
                    sf = SubstitutesFinder()
                    sub = sf.get_substitutes(product["nutrition_grade"], category_id[0])
                    print(f" Votre substitue choisi : {sub[1]}")
                    save_choice = int(input(
                        "1 - Sauvegarder mon produit dans mes favoris. \n"
                        "2 - Retourner au menu principale. \n"
                    ))
                    if save_choice == 1:
                        sp = SaveProducts()
                        save_user_prod = sp.save_user_product(product["id"], sub[0])
                    if save_choice == 2:
                        Main.main_screen()

                if choice == 2:
                    fav = Favorites()
                    fav_table = fav.get_products_from_favorite()

                if choice == 3:
                    loop = 0
            except ValueError:
                return self.main_screen()

if __name__=="__main__":
    Main()
