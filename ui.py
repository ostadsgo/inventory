import os
from enum import Enum
from shop import Shop
from models import Product


class Menu(Enum):
    """
    Menu options
    """

    ADD = "add"
    SHOW = "show"
    HELP = "help"
    REMOVE = "remove"
    SEARCH = "search"
    CLEAR = "clear"
    SORT_ASC = "sort asc"
    SORT_DEC = "sort dec"
    EXIT = "exit"


class Ui:
    """User interfece that user will interact."""

    @staticmethod
    def clear_screen():
        """Clear console screen."""
        os.system("cls")

    @staticmethod
    def show_logo() -> str:
        """Simple text to repersent logo of the app."""
        return """
            *******************
            ** SHOPPING_LIST **
            *******************
        """

    @staticmethod
    def make_menu() -> str:
        """Iterate over Menu enum and create menu items.
        Returns:
        --------
        outs:
            Return menu items as a string.

        """
        print("Menu items: ")
        print("-" * 30)
        items = ""
        for menu_item in Menu:
            items += f" -  {menu_item.value}\n"
        return items

    @staticmethod
    def add_ui():
        """
        Get product info from user and pass them to save method
        to save the prodect.
        """
        name = input("Enter product name:").lower()
        number = int(input("Enter number of the products: "))
        price = int(input("Enter price of the product: "))
        result = Shop.save(name, number, price)
        if result:
            print("Product saved successfully.")
        else:
            print("Some problem happend. Look at log file.")

    @staticmethod
    def remove_ui():
        """Get input from user to delete a product."""
        name = input("Product name: ").lower()
        result = Shop.remove(name)
        if result:
            print("The product delete successfuly.")
        else:
            print("Product not found!")

    @staticmethod
    def search_ui():
        """Input product name to search throughout products."""
        name = input("Product name: ").lower()
        product = Shop.search(name)
        if product:
            print(product)
        else:
            print("Product not found!!")

    @classmethod
    def display(cls, products: list[Product]):
        """Get list of poducts and create table like output and print it.

        Parameters
        -----------
            products: list of products

        """
        titles = ("Product Name", "Quantity", "Price", "Total Price")
        header = "{:<30}{:<10}{:>20}{:>20}".format(*titles)
        dashes = "-" * len(header)
        print(f"{header}\n{dashes}")

        for product in products:
            s = "{:<30}{:<10}{:>20}${:>20}$"
            val = (
                product.name,
                product.quantity,
                product.price,
                product.quantity * product.price,
            )
            print(s.format(*val))
        print(dashes)
        total_capital = Shop.total_capital()
        quantities = Shop.total_quantities()
        footer = "{:>31}{:>50}$".format(quantities, total_capital)
        print(footer)

    @staticmethod
    def show_ui():
        """Display all products in the screen."""
        products = Shop.products()
        Ui.display(products)

    @staticmethod
    def help_ui():
        """Print help mannual in the screen."""
        print(Shop.mannual())

    @staticmethod
    def sort_asc_ui():
        """Display sorted products ascengingly by name in the screen."""
        products = Shop.sort_asc()
        Ui.display(products)

    @staticmethod
    def sort_dec_ui():
        """Display sorted products descengingly by name in the screen."""
        products = Shop.sort_dec()
        Ui.display(products)

    @staticmethod
    def exit_ui():
        """Exit of the program."""
        print("Goodbye.")
        exit()

    @classmethod
    def initial(cls):
        """Clear screen print log and make menu and print it."""
        cls.clear_screen()
        print(cls.show_logo())
        print(cls.make_menu())

    @classmethod
    def menu(cls):
        """Display menu and get user response and act based on."""
        while True:
            Ui.initial()
            response = input("> ")

            if response == Menu.EXIT.value:
                Ui.exit_ui()
            elif response == Menu.ADD.value:
                Ui.add_ui()
            elif response == Menu.SHOW.value:
                Ui.show_ui()
            elif response == Menu.HELP.value:
                Ui.help_ui()
            elif response == Menu.REMOVE.value:
                Ui.remove_ui()
            elif response == Menu.SEARCH.value:
                Ui.search_ui()
            elif response == Menu.CLEAR.value:
                Ui.clear_screen()
            elif response == Menu.SORT_ASC.value:
                Ui.sort_asc_ui()
            elif response == Menu.SORT_DEC.value:
                Ui.sort_dec_ui()
            else:
                print("Wrong choice!!")

            input("\nPress Enter key to continue ....")
