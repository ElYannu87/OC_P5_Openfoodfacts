from typing import List, Tuple


class Menu:
    """
    Dynamic menu shared throughout the whole program
    """

    def __init__(self, message: str, prompt: str, elements: List[Tuple[int, str]]):
        self.result = self.menu_selector(message, prompt, elements)

    def display_menu(self, message: str, elements: List[Tuple[int, str]]):
        """
        Displays the menu to the user
        ---------------------------------
        :param message: takes a customized message to show to the user
        :param elements: takes the elements to choose from in from if a List
        :return: Displays the menu that contains the 'message' and the 'elements'
        """
        print(message)
        for index, value in enumerate(elements):
            print(f"{index + 1}) {value[1]}")
        print()

    def select_menu_element(self, prompt: str, elements: List[Tuple[int, str]]):
        """
        Asks the user to make a choice from the different options on display.
        Includes a safety against wrong inputs and will be recursive until a proper input is made
        ---------------------------------
        :param prompt: users previous input
        :param elements:
        :return:
        """
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
        """
        Calls both of the upper functions
        :param message: takes the previous message
        :param prompt: takes the user input
        :param elements: uses the the different elements given in a List
        :return: the elements chosen by the user
        """
        self.display_menu(message, elements)
        element_index = self.select_menu_element(prompt, elements)
        return elements[element_index]
