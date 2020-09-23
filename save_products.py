import psycopg2
from psycopg2 import extras
from config import *


conn = psycopg2.connect(dbname=DB, user=DB_USER, password=DB_PW, host=HOST, port=PORT)



class SaveProducts:

    def save_user_product(self, product):
        pass

    def drop_user_product(self,product):
        pass
