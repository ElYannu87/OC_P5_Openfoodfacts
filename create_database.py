import psycopg2
from psycopg2 import extras

from config import DB, DB_PW, DB_USER, HOST, PORT


class CreateDatabase:
    """
    Creates the Database if none existent
    Each table will check before it's creation if it is already
    present in the Database.
    """

    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)

    def check_table_exists(self, table_name):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT EXISTS(SELECT FROM information_schema.tables WHERE table_schema = 'public' "
                       "AND table_name = %s)", [table_name])
        exists = cursor.fetchone()
        if exists:
            print(f'{table_name} already exists')
        return exists

    def category_table(self):
        if self.check_table_exists("category"):
            return
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("CREATE TABLE IF NOT EXISTS category(id SERIAL NOT NULL CONSTRAINT category_pk PRIMARY KEY,tag  "
                       "TEXT,name TEXT   NOT NULL,url  TEXT   NOT NULL);")
        cursor.close()

    def product_table(self):
        if self.check_table_exists("product"):
            return
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("CREATE TABLE IF NOT EXISTS product(id SERIAL NOT NULL CONSTRAINT product_pk PRIMARY KEY, name "
                       "TEXT   NOT NULL, store TEXT, nutrition_grade CHAR NOT NULL, url TEXT   NOT NULL);")
        cursor.close()

    def favorite_table(self):
        if self.check_table_exists("favorite"):
            return
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("CREATE TABLE IF NOT EXISTS favorite (source_product_id INTEGER NOT NULL CONSTRAINT "
                       "favorite_source_product_id_fk REFERENCES product, replacement_product_id "
                       "INTEGER NOT NULL CONSTRAINT favorite_replacement_product_id_fk REFERENCES product, CONSTRAINT "
                       "favorite_pk PRIMARY KEY (source_product_id, replacement_product_id));")
        cursor.close()

    def product_category_table(self):
        if self.check_table_exists("product_category"):
            return
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("CREATE TABLE IF NOT EXISTS product_category (product_id INTEGER NOT NULL CONSTRAINT "
                       "product_category_product_id_fk REFERENCES product, category_id INTEGER NOT NULL CONSTRAINT "
                       "product_category_category_id_fk REFERENCES category, CONSTRAINT product_category_pk PRIMARY "
                       "KEY (product_id, category_id));")
        cursor.close()
