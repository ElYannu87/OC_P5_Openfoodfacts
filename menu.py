from typing import List, Tuple


class Menu:

    def __init__(self, message: str, prompt: str, elements: List[Tuple[int, str]]):
        self.result = self.menu_selector(message, prompt, elements)

    def display_menu(self, message: str, elements: List[Tuple[int, str]]):
        print(message)
        for index, value in enumerate(elements):
            print(f"{index + 1}) {value[1]}")
        print()

    def select_menu_element(self, prompt: str, elements: List[Tuple[int, str]]):
        result = input(prompt)  # type: str
        try:
            result_index = int(result) - 1
            if result_index < 0 or result_index >= len(elements):
                return self.select_menu_element(prompt, elements)
            else:
                return result_index
        except ValueError:
            return self.select_menu_element(prompt, elements)

    def menu_selector(self, message: str, prompt: str, elements: List[Tuple[int, str]]):
        self.display_menu(message, elements)
        element_index = self.select_menu_element(prompt, elements)
        return elements[element_index]

# menu = Menu("Liste des produits", "choisissez un produit: ", ["orange", "banane", "pomme"])
# print(menu.result)
