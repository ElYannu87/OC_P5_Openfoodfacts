from typing import Tuple, List
from menu import Menu
from database_browser import DatabaseBrowser


class Controller:
    """
    Ask user for a category and a product
    ---------------------------------
    All functions use the dynamic menu.py
    """

    def categories_browser(self) -> Tuple[int, str]:
        """
        Fetches for the most popular categories
        ---------------------------------
        :returns the id of the chosen category
        """
        db = DatabaseBrowser.get_instance()
        query_result = db.get_categories()
        menu_elements = list()  # type: List[Tuple[int, str]]
        for e in query_result:
            menu_elements.append((e[0], e[1]))
        menu = Menu("Liste des categories", "choisissez une catégorie: ", menu_elements)
        category_chosen = menu.result  # type: Tuple[int, str]

        return category_chosen

    def product_browser(self, category_id: int):
        """
        Returns all the products contained in the chosen category, showing the nutrition grade in order to give
        the user the choice for a product
        ---------------------------------
        :param category_id returned from the user choice in categories_browser
        :returns a dictionnary with the product id, the product name and the nutrition grade
        """
        db = DatabaseBrowser.get_instance()
        product_result = db.get_products(category_id)
        menu_elements = list()      # type: List[Tuple[int, str]]
        for e in product_result:
            menu_elements.append((e[2], f"{e[0]} : {e[1]}"))
        menu = Menu("Liste des produits", "choisissez un produit: ", menu_elements)
        selected_product = menu.result
        database_product = product_result
        i = 0
        while selected_product[0] != database_product[i][2]:
            i = i + 1

        return {"id": database_product[i][2], "name": database_product[i][0], "nutrition_grade": database_product[i][1]}

    def substitute_browser(self, product_ng, category_id):
        """
        Compares the product chosen by the user to find a better alternative by comparing the nutrition grade
        ---------------------------------
        :param product_ng: nutrition grade
        :param category_id: category id
        :return: all products in the same category with a better nutrition grade
        """
        db = DatabaseBrowser.get_instance()
        substitute_result = db.get_substitutes(product_ng, category_id)
        menu_elements = list()
        for e in substitute_result:
            menu_elements.append((e[2], f"{e[1]} : {e[0]}"))
        menu = Menu("Liste des produits", "choisissez un substitue: ", menu_elements)
        substitutes_choice = menu.result
        database_product = substitute_result
        i = 0
        while substitutes_choice[0] != database_product[i][2]:
            i = i + 1

        return substitutes_choice

    def save_products(self, product, sub):
        """
        Saves the chosen product and the substitute into the favorite table in the Database
        ---------------------------------
        :param product: The initially chosen product
        :param sub: the chosen substitute
        """
        db = DatabaseBrowser.get_instance()
        save_user_product = db.save_user_product(product, sub)

        return save_user_product

    def show_favorites(self):
        """
        Shows all of the saved favorite substitutes of the user
        :return: A list of all the saved substitutes with their name, nutrition grade, where to buy and the URL for
                 more information on the product
        """
        db = DatabaseBrowser.get_instance()
        query_result = db.get_products_from_favorite()
        favorite_db_products = []
        for element, index, id, name, store, nutri, url in query_result:
            print(f"Nom : {name} \n Magasin : {store} \n Grade nutritionnel : {nutri} \n URL : {url} \n")

        return favorite_db_products
