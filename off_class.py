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
