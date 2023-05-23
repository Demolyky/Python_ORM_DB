from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# проверка структуры БД и ее создание
class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    id_publisher = Column(Integer, ForeignKey('publisher.id'))
    publisher = relationship(Publisher, backref='books')

class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    id_shop = Column(Integer, ForeignKey('shop.id'))
    id_book = Column(Integer, ForeignKey('book.id'))
    count = Column(Integer)

class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    price = Column(Numeric)
    date_sale = Column(DateTime)
    count = Column(Integer)
    id_stock = Column(Integer, ForeignKey('stock.id'))
    stock = relationship(Stock, backref='sales')
