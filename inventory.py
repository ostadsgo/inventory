import os
import tomllib
import logging
from enum import Enum
from dataclasses import dataclass
from typing import Tuple


# basic config for log file.
logging.basicConfig(filename="inventory.log", encoding="utf-8", level=logging.DEBUG)


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


@dataclass
class ProductFile:
    """
    File operations for Product class
    filename must be provided to create a file.
    """

    filename: str

    def append(self, line: str) -> bool:
        """
        recive a line of text and append it to the end of the file.

        Parameters
        ----------
        line: str
            text to write to the file.

        Returns
        -------
        out: bool
            Return True if write operation was successful otherwise False

        """
        try:
            with open(self.filename, "a") as file:
                file.write(line)
                return True
        except FileExistsError as e:
            logging.error(str(e))
        except Exception as e:
            logging.error(str(e))
        return False

    def write(self, lines: list[str]):
        """
        Iterate over line of text and write them to the file.

        Parameters
        ----------
        lines: list[str]
            List of lines each line is just a normal text

        Returns
        -------
        out: bool
            Return True if write operation was successful otherwise False
        """
        try:
            with open(self.filename, "w") as file:
                file.write(lines)
                return True
        except FileExistsError as e:
            logging.error(str(e))
        except Exception as e:
            logging.error(str(e))
        return False

    def read(self) -> list[str]:
        """
        Read content of the filename and return them as list of text

        Returns
        -------
        out: bool
            Return list of string if able to read filename's content otherwise return empty list
        """
        # default content
        content = []
        try:
            with open(self.filename) as file:
                content: list[str] = file.read().strip().split("\n")
        except FileNotFoundError:
            logging.error("inventory.txt is not exist.")
        except Exception as e:
            print(f"Wired exceptions happend! {e}")

        return content


@dataclass
class Product:
    """
    Represent a product.
    A product consist of name, number and price
    Name of the product to create a product is required.
    """

    # default filename to store products
    FILENAME = "inventory.txt"

    def __init__(self, name: str, number=0, price=0):
        self.name = name
        self.number = number
        self.price = price
        self.total_price = self.number * self.price
        self.productfile = ProductFile(self.FILENAME)

    def calc_total_price(self) -> int:
        """
        Calculate total price of the product

        Returns
        -------
        out: int
            Return totoal price of the product.
        """
        self.total_price = self.price * self.number
        return self.total_price

    def save(self) -> bool:
        """
        Save the product in the file. Take log if there was exceptions.

        Returns
        -------
        out: bool
            Return True if product save successfully otherwise False.

        """
        line = f"{self.name},{self.number},{self.price},{self.calc_total_price()}\n"
        if self.productfile.append(line):
            return True
        return False

    def is_exist(self) -> int:
        """
        Check if product is already exist in the file or not

        Returns
        -------
        outs: int
            Retrun the index of the product if found otherwise -1
        """
        products: list[str] = self.productfile.read()
        for index, product in enumerate(products):
            name, *_ = product.split(",")
            if name == self.name:
                return index
        return -1

    def add(self) -> bool:
        """
        Check if product is not in the file add it.

        Returns
        -------
        out: bool
            Return True if file saved otherwise return False
        """
        if self.is_exist() >= 0:
            return False
        return True if self.save() else False

    def remove(self):
        """
        Remove a product if exist.

        Returns
        -------
        out: bool
            True if remove operation was successful otherwise False.
        """
        products: list[str] = self.productfile.read()
        index = self.is_exist()
        if index == -1:
            return False
        del products[index]
        self.productfile.write(products)
        return True

    def search(self) -> str:
        """
        Search product by name.

        Returns
        -------
        outs: str
            Return the product if found otherwise return empty sting
        """
        products: list[str] = self.productfile.read()
        index = self.is_exist()
        if index == -1:
            return ""
        return products[index]

    @classmethod
    def sort_asc(cls):
        """
        Sort products ascending
        """
        file = ProductFile(filename=cls.FILENAME)
        products: list[str] = file.read()
        sorted_products: list[Product] = sorted(products)
        cls.display(sorted_products)

    @classmethod
    def sort_dec(cls):
        """Sort products descending"""
        file = ProductFile(filename=cls.FILENAME)
        products: list[str] = file.read()
        sorted_products: list[Product] = sorted(products, reverse=True)
        cls.display(sorted_products)

    @classmethod
    def show(cls):
        """Show all products."""
        file = ProductFile(cls.FILENAME)
        products = file.read()
        cls.display(products)

    @staticmethod
    def display(products: list[str]):
        """
        Get list of products and print them in a table like format.
        """
        header = f"{'Product Name':20}{'Quantity':10}Price\tTotal Price"
        dashes = "-" * len(header)
        print(f"{header}\n{dashes}")
        prod_total_num = 0
        for product in products:
            # if product was true value
            if product:
                name, number, price, total_price = product.split(",")
                print(f"{name:20}{number:10}${price}\t${total_price}")
                prod_total_num += int(number)
                print(f"Total number of products: {prod_total_num}")
            else:
                print("No Products. or wrong product format.")

    @staticmethod
    def manual():
        """
        Display help on how to use the program
        """
        return """
        Copy right by Zahra Mohammadzadeh
        Last Edit: 2023/1/26
        An application to manage an inventory of the shop.
        Features:
        - User authorization.
        - Opetions like add, remove, search and show products.
        Press `exit` to exit out of the program.
        """


@dataclass
class User:
    """
    Authorized user management
    """

    username: str
    password: str

    def read_config(self):
        """ """
        with open("config.toml", "rb") as toml_file:
            config = tomllib.load(toml_file)
        return config

    @staticmethod
    def input_credentials() -> Tuple[str, str]:
        """Ask user to give username and password."""
        username = input("Username: ")
        password = input("Password: ")
        return username, password

    def admin_credentials(self) -> Tuple[str, str]:
        """
        Extract admin username and admin password

        Returns
        -------
        outs: str, str
            Return admin username and password.
        """
        config = self.read_config()
        username = config.get("username")
        passwd = config.get("password")
        return username, passwd

    def check_passwd(self) -> bool:
        """
        Compare username and password with the admin credentials

        Retruns:
        --------
        outs: bool
            True if user reponse credentials was correct otherwise False
        """
        admin_username, admin_passwd = self.admin_credentials()

        if self.username == admin_username and self.password == admin_passwd:
            return True
        return False


class Ui:
    """
    User interfece that user will interact.
    """

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
    def show_menu():
        """Iterate over Menu enum and create menu items.
        Returns:
        --------
        outs:

        """
        print("Menu items: ")
        print("-" * 30)
        items = ""
        for menu_item in Menu:
            items += f" -  {menu_item.value}\n"
        return items

    @staticmethod
    def add_ui() -> Product | None:
        """
        Get product info from user.

        Returns:
        --------
        Outs: Product or None
            Return a product if user response was correct otherwise None
        """
        try:
            name = input("Enter product name:").lower()
            number = int(input("Enter number of the products: "))
            price = int(input("Enter price of the product: "))
            product = Product(name, number, price)
            if product.add():
                print("Product add successfuly.")
            else:
                print("Problem!!Product didn't add to the file")
        except ValueError:
            print("Error, please enter a valid number.")
            logging.error("wrong value for product number.")
        except Exception as e:
            print(e)
            logging.info(str(e))

    @staticmethod
    def remove_ui():
        """Get input from user to delete a product."""
        name = input("Product name: ").lower()
        product = Product(name=name)
        if product.remove():
            print(f"{product.name} deleted successfully.")

    @staticmethod
    def search_ui():
        """Input product name to search throughout products."""
        name = input("Product name: ").lower()
        product = Product(name=name)
        result = product.search()
        if result:
            print(result)
        print("Product not found!!")

    @staticmethod
    def show_ui():
        Product.show()

    @staticmethod
    def help_ui():
        print(Product.manual())

    @staticmethod
    def sort_asc_ui():
        Product.sort_asc()

    @staticmethod
    def sort_dec_ui():
        Product.sort_dec()

    @staticmethod
    def exit_ui():
        print("Goodbye.")
        exit()

    @classmethod
    def menu(cls):
        """Display menu and get user response and act based on."""
        while True:
            cls.clear_screen()
            print(cls.show_logo())
            print(cls.show_menu())
            response = input("> ")

            if response in Menu.EXIT.value:
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


def main():
    """Main function to run the program."""
    for _ in range(3):
        username, password = User.input_credentials()
        user = User(username, password)
        if user.check_passwd():
            Ui.menu()
        else:
            print("Username or password is incorrect.")


if __name__ == "__main__":
    main()
