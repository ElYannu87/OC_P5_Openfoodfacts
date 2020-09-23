class Category:
    """ Class representing the category table of the database """

    def __init__(self, tag, name, url):
        self.tag = tag
        self.name = name
        self.url = url


class Product:
    """ Class representing the product table of the database """

    def __init__(self, name, store, nutrition_grade, url, category):
        self.name = name
        self.store = store
        self.nutrition_grade = nutrition_grade
        self.url = url
        self.category = category


class ProductCategory:

    def __init__(self, product_id, category_id, count):
        self.product_id = product_id
        self.category_id = category_id
        self.count = count
