import psycopg2
from psycopg2 import extras
from config import *


conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

new_data = 0
products_list = []
categories_list = []

class SaveProducts:

    def drop_user_product(self,product):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "DELETE FROM favorite WHERE name = '%s' "
        cur.execute(sql % product.name)
        cur.close()
        conn.commit()
        print("\nProduit supprimé de votre liste.")


    def save_user_product(self, product):
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
