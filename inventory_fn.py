import os
from enum import Enum
from dataclasses import dataclass
import logging
import tomllib


EXIT_COMMANDS = ["q", "quit", "ex", "exit"]
shopping_list = list()

logging.basicConfig(filename="shop_app.log")


class Menu(Enum):
    """Menu options."""

    add = "add"
    show = "show"
    help = "help"
    remove = "remove"
    search = "search"
    clear = "clear"
    sort_asc = "sort asc"
    sort_dec = "sort dec"


@dataclass
class Product:
    """Represent a Product"""

    name: str
    price: int
    number: int = 1
    total_price: int = 0


def total_price(price: int, number: int) -> int:
    """
    Return total price for a product

    Parameters
    ----------
    price: int
        Price of the product
    number: int
        Number of the product

    Returns
    ------
    out: int
        total price of a product
    """
    return price * number


def append_product(product: str):
    """
    Append  a product to the inventory.txt

    Parameters
    ----------
    product: str
        Product is a string contains product's attributes separated with comma

    Returns
    ------
    out: None
        Return nothing if there was FileNotFoundError get a log message.
    """
    try:
        with open("inventory.txt", "a") as file:
            row: str = f"{product.name},{product.item_number},"
            row += f"{product.price},{product.total_price}\n"
            file.write(row)
    except FileNotFoundError:
        logging.error("inventory.txt not found!")


def write_products(products: list[Product]):
    """
    Write products in the `inventory.txt` file.
    Parameters
    ----------
    products: list[Product]
        List of products; Each product is a object of Product class.

    Returns
    -------
        Return nothing if there was FileNotFoundError write a log message.
    """
    try:
        with open("inventory.txt", "w") as file:
            for product in products:
                file.write(product)
    except FileNotFoundError:
        logging.error("inventory.txt not found!")


def read_products():
    """
    Read content of `inventory.txt` file.
    Returns
    -------
    out: str or None
        Return product list, each product is a string separated by comma
        if there `inventory.txt` was exist write log message.
    """
    try:
        with open("inventory.txt", "r") as file:
            content: list[Product] = file.readlines()
            return content
    except FileNotFoundError:
        logging.error("inventory.txt not found!")


def add_product(name: str, price: int, item_number: int):
    """
    Create Product object and pass it to the append_product to write that in the file.
    Parameters
    ----------
    name: str :
        name of the product
    price: int :
        price of the product
    item_number: int :
        number of the product.

    Returns
    -------
        out: Return nothing
    """
    products = read_products()
    for product in products:
        p_name, *rest = product.split(",")
        if p_name == name:
            print("Item is already in the shop.")
            return None
    product = Product(
        name,
        price,
        item_number,
        total_price(price, item_number),
    )
    # append product to end of the file.
    append_product(product)


def show_products():
    """
    Read all product and display them in table like format.
    """
    products: list[Product] = read_products()
    print(f"{'Product Name':20}{'Quantity':10}Price\tTotal Price")
    print("-" * 50)
    item_numbers: int = 0
    for product in products:
        name, number, price, total_price = product.split(",")
        print(f"{name:20}{number:10}${price}\t${total_price}", end="")
        item_numbers += int(number)
    print(f"All items number are: {item_numbers}")


def remove_product(item: str):
    """
    Get product name if product found delete it and write new list to the file.
    Parameters
    ----------
    item: str :
        product name

    Returns
    -------
        out: return nothing if product was not found appropriate message.
    """
    products: list[Product] = read_products()
    for product in products.copy():
        name, *rest = product.split(",")
        if name == item:
            products.remove(product)
            print(f"{item} delete successfully.")
            break
    else:
        print("item that you are trying to remove is not in the list")

    write_products(products)


def search_product(product_name: str):
    """
    Compare product_name with name of the all product if found the product
    print `found` if not found print `not found`
    Parameters
    ----------
    product_name: str :
        name of the product
    """
    products: list[Product] = read_products()
    for product in products:
        name, *rest = product.split(",")
        if product_name == name:
            print(product)
            break
    else:
        print(f"{product_name} not found")


def show_help():
    """
    Display help for the program.
    """
    print("enter, `QUIT` to exit the app and see your list")
    print("enter, `HELP` to see help")


def sort_product_ascending():
    """
    Read all products form `inventory.txt` and sort them by name ascending.
    """
    products: list[Product] = read_products()
    sorted_products: list[Product] = sorted(products)
    print(f"{'Product Name':20}{'Quantity':10}Price\tTotal Price")
    print("-" * 50)
    for product in sorted_products:
        name, number, price, total_price = product.split(",")
        print(f"{name:20}{number:10}${price}\t${total_price}", end="")


def sort_product_descending():
    """
    Read all products form `inventory.txt` and sort them by name descending.
    """
    products: list[Product] = read_products()
    sorted_products: list[Product] = sorted(products, reverse=True)
    print(f"{'Product Name':20}{'Quantity':10}Price\tTotal Price")
    print("-" * 50)
    for product in sorted_products:
        name, number, price, total_price = product.split(",")
        print(f"{name:20}{number:10}${price}\t${total_price}", end="")


def clear_screen():
    """
    Clear console screen.
    """
    return os.system("CLS")


def read_config():
    """
    Read toml config file.

    Return
    ------
    out: Dict[str,str]
        Return python dict contains all configs as key value pair.
    """
    with open("config.toml", "rb") as toml_file:
        config = tomllib.load(toml_file)
    return config


def check_passwd(
    admin_username: str,
    admin_password: str,
    username: str,
    password: str,
) -> bool:
    """
    Compare user response username and password with admin username and password.
    Parameters
    ----------
    admin_username : str
        username of the admin
    admin_password : str
        password of the admin
    username: str :
        username
    password: str :
        password

    Returns
    -------
        out: bool
        Reutrn True if useranem and password will equal with admin's useranme and password
        otherwise returns False.
    """
    if username == admin_username and password == admin_password:
        return True
    return False


def menu():
    """
    Main function to request user option from user
    If user choose from menu will run the corresponding function
    Otherwise print `wrong choice`.
    """
    while True:
        clear_screen()
        app_logo = """
        *******************
        ** SHOPPING_LIST **
        *******************
        """
        print(app_logo)
        print("Menu items: ")
        print("-" * 30)
        items = ""
        for shopping in Menu:
            items += " - " + shopping.value + "\n"
        print(items)
        item = input("> ")
        if item in EXIT_COMMANDS:
            break
        elif item == Menu.add.value:
            # name = input("Enter product name:")
            try:
                name = input("Enter product name:").lower()
                item_number = int(input("Enter item number: "))
                price = int(input("Enter price of the product: "))
                add_product(name, price, item_number)
            except ValueError:
                print("Error, please enter a valid number.")
                logging.error("wrong value for item_number.")
        elif item == Menu.show.value:
            show_products()
        elif item == Menu.help.value:
            show_help()
        elif item == Menu.remove.value:
            item_to_remove = input("Enter item name to remove:")
            remove_product(item_to_remove)
        elif item == Menu.search.value:
            item_to_search = input(
                "please enter the item that you want to search:"
            ).lower()
            search_product(item_to_search)
        elif item == Menu.clear.value:
            clear_screen()
        elif item == Menu.sort_asc.value:
            sort_product_ascending()
        elif item == Menu.sort_dec.value:
            sort_product_descending()
        else:
            print("Wrong choice!!")
            logging.info("user chooses wrong option", item)

        input("\nPress Enter key to continue ....")


def authorization():
    """
    Get username and password from user and compare it with admin's username and password
    User will prompt to add username and password for 3 time.
    """
    config = read_config()
    admin_username = config["username"]
    admin_password = config["password"]
    for i in range(3):
        username = input("Username: ")
        password = input("Password: ")
        if check_passwd(admin_username, admin_password, username, password):
            menu()
            break
        else:
            print("Username or password is incorrect.")


def main():
    """Program will start from this funciton."""
    authorization()


# first function to run.
main()
