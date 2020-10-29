import psycopg2
from psycopg2 import extras
import requests
from config import *


class FillDatabase:
    """
    Class using two functions in order to fill the database
    """

    def __init__(self):
        """
        Executes at first the inserts for the categories and then the products into the Database
        """
        self.conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)
        self.categories = self.fill_category()
        self.fill_products()

    def check_table_not_empty(self, table_name):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT COUNT(*) FROM %s", (table_name,))
        count = cursor.fetchone
        if count:
            print("Database has content")
        return count > 0

    def fill_products(self):
        """
        Searches the .json of openfoodfacts for products and insert those into the product table of the
        Database
        """
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        categories = dict()
        for page in range(1, 2):
            result = requests.get(
                'https://fr.openfoodfacts.org/cgi/search.pl?page_size=1000&page={}&action=process&json=1'.format(
                    page)).json()
            for element in result['products']:
                try:
                    cursor.execute(
                        "INSERT INTO product (name, store, nutrition_grade, url) VALUES (%s, %s, %s, %s) RETURNING "
                        "id, name",
                        (element["product_name"], element["stores"], element["nutrition_grade_fr"], element["url"]))
                    # un except pour éviter les erreurs de clés
                    query_result = cursor.fetchone()
                    for category in element["categories_tags"]:
                        try:
                            cursor.execute("INSERT INTO product_category(product_id, category_id) VALUES (%s, %s)",
                                           (query_result[0], self.categories[category]))
                        except KeyError:
                            print("Categorie insertion failed")

                    print(element["product_name"])
                except KeyError:
                    print(f'product insertion failed:')

        self.conn.commit()
        cursor.close()

    def fill_category(self):
        """
        Searches the different categories on openfoodfacts and inserts them into the category table in the Database
        :return: Categories
        """
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        categories = dict()
        result = requests.get('https://fr.openfoodfacts.org/categories.json').json()
        for element in result['tags']:
            try:
                cursor.execute("INSERT INTO category (tag, name, url) VALUES  (%s, %s, %s) RETURNING id, tag",
                               (element["id"], element["name"], element["url"]))
                query_result = cursor.fetchone()
                categories.__setitem__(query_result[1], query_result[0])
            except self.conn.OperationalError:
                print("operation Error")
            except self.conn.DataError:
                print("Data Error")
        self.conn.commit()
        cursor.close()
        return categories


FillDatabase()
