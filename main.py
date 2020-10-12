from controller import Controller
from substitues import SubstitutesFinder
from save_products import SaveProducts
from favorites import Favorites
from config import *
import psycopg2


class Main:
    """
    Enables the whole script
    """
    def __init__(self):
        """
        Calls both functions in order
        """
        self.check_database()
        self.main_screen()

    def check_database(self):
        """
        Enables the script to check if there is any content in the Database to avoid filling it at each use
        """
        connection = None
        try:
            connection = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)
            print('Database connected.')

        except:
            print('Database not connected.')
        cur = connection.cursor()

        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public'"
                    "AND table_name = 'category')")

        list_database = cur.fetchall()

    def main_screen(self):
        """
        Main menu that guides the user to the different functionalities of the program and will execute only the chosen
        option
        """
        loop = 1
        while loop:
            try:
                choice = int(input(
                    "1 - Choisir des aliments à substituer. \n"
                    "2 - Voir mes favoris. \n"
                    "3 - Quitter le programme. \n"
                ))
                if choice == 1:
                    cb = Controller()
                    category_id = cb.categories_browser()
                    product = cb.product_browser(category_id[0])
                    sf = cb.substitute_browser
                    sub = cb.substitute_browser(product["nutrition_grade"], category_id[0])
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


if __name__ == "__main__":
    Main()
