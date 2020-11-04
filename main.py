from controller import Controller


class Main:
    """
    Enables the program
    """

    def __init__(self):
        """
        Calls both functions in order
        """
        self.main_screen()

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
                cb = Controller()
                if choice == 1:
                    category_id = cb.categories_browser()
                    product = cb.product_browser(category_id[0])
                    sub = cb.substitute_browser(product["nutrition_grade"], category_id[0])
                    print(f" Votre substitue choisi : {sub[1]}")
                    save_choice = int(input(
                        "1 - Sauvegarder mon produit dans mes favoris. \n"
                        "2 - Retourner au menu principale. \n"
                    ))
                    if save_choice == 1:
                        cb.save_products(product["id"], sub[0])
                    if save_choice == 2:
                        Main.main_screen(self)

                if choice == 2:
                    cb.show_favorites()

                if choice == 3:
                    loop = 0
            except ValueError:
                return self.main_screen()


if __name__ == "__main__":
    Main()
