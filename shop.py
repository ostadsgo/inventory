import logging
from dataclasses import dataclass

from models import Product as ProductModel
from models import session

logging.basicConfig(
    filename="shop.log",
    encoding="utf-8",
    level=logging.DEBUG,
)


@dataclass
class Shop:
    """
    Shop management
    """

    # default filename to store products
    FILENAME = "shop.db"

    @classmethod
    def save(cls, name: str, quantity=0, price=0) -> bool:
        """
        Get product name, quntity and price and if it is not exist
        save it in the database

        Returns
        -------
        out: bool
            Return True if product save successfully otherwise False.

        """
        # TODO: check product exist or not;
        # if product is not saved then you will save it;

        try:
            product = ProductModel(name=name, quantity=quantity, price=price)
            session.add(product)
            session.commit()
            return True
        except Exception as e:
            logging.error(f"Error on save: {e}")
            return False

    @classmethod
    def remove(cls, name: str) -> bool:
        """Execuate a query to find the give name

        Parameters
        -----------
        name: str
            Product name to delete

        Returns
        -------
        outs: bool
            Return True if delete operation was successful otherwise False
        """
        try:
            product = session.query(ProductModel).filter_by(name=name).one()
            session.delete(product)
            session.commit()
            return True
        except Exception as e:
            logging.error(f"Error on remove {e}")
            return False

    @classmethod
    def search(cls, name: str) -> str:
        """Execute a qurey to find product.
         Parameters
        -----------
        name: str
            Product name to find

        Returns
        -------
        outs: str
            Return the product object if product was found
            otherwise return empty string

        """
        try:
            product = session.query(ProductModel).filter_by(name=name).one()
            s = "Name: {}\nQuntity: {}\nPrice: {}\n"
            val = (product.name, product.quantity, product.price)
            result = s.format(*val)
            return result

        except Exception as e:
            logging.error(f"Error on search {e}")
            return ""

    @classmethod
    def products(cls):
        products = session.query(ProductModel).all()
        return products

    @classmethod
    def mannual(cls):
        """
        Display help on how to use the program
        """
        s = """
        Copy right by Zahra Mohammadzadeh
        Last Edit: 2023/1/26
        An application to manage an inventory of the shop.
        Features:
        - User authorization.
        - Opetions like add, remove, search and show products.
        Press `exit` to exit out of the program.
        """
        return s

    @classmethod
    def sort_asc(cls) -> list[ProductModel]:
        """Retrieve all products and sort them ascendingly.

        Returns
        -------
        outs: list[Product]
            Return list of products
        """
        products = session.query(ProductModel).order_by(ProductModel.name)
        return products

    @classmethod
    def sort_dec(cls):
        """Retrieve all products and sort them descendingly.

        Returns
        -------
        outs: list[Product]
            Return list of products sorted descending.
        """
        return Shop.sort_asc()[::-1]

    @classmethod
    def total_capital(cls) -> int:
        """Calculate total capital of shop.

        Returns
        --------
        outs: int
            Return total capital
        """
        total = 0
        products = session.query(ProductModel).all()
        for product in products:
            total += product.price * product.quantity
        return total

    @classmethod
    def total_quantities(cls):
        """Calculate total capital of shop.

        Returns
        --------
        outs: int
            Return total of quantities.
        """
        total = 0
        products = session.query(ProductModel).all()
        for product in products:
            total += product.quantity
        return total
