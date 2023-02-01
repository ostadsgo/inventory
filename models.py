from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Product(Base):
    """Product model."""

    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(Integer)
    price = Column(Integer)

    def __repr__(self) -> str:
        s = "Product(id={}, name={}, quantity={}, Price={})"
        return s.format(self.id, self.name, self.quantity, self.price)


# create connection
engine = create_engine("sqlite:///shop.db")
Session = sessionmaker(bind=engine)
session = Session()
# create database
Base.metadata.create_all(engine)
