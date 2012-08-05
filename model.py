"""
    Model classes for the financials program
"""

# Standard library
import os, sys
import argparse
import logging

# Third-party
import sqlalchemy as sqy
from sqlalchemy import Column, Table, ForeignKey, UniqueConstraint
from sqlalchemy import Integer, String, Float, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

__author__ = "adrn@astro.columbia.edu"

logger = logging.getLogger(__name__)

f = open("config", "r")
for line in f.readlines():
    key,val = line.split()
    
    if key == "db_file":
        db_filename = val
        break

engine = sqy.create_engine(os.path.join("sqlite:///", db_filename), echo=False)
Base = declarative_base(bind=engine)

class Stock(Base):
    __tablename__ = 'stock'
    
    id = Column("id", Integer, primary_key=True)
    symbol = Column("symbol", String(8), unique=True)
    name = Column("name", String(20))
    
    def __init__(self, symbol, name):
        """ Takes a stock symbol, e.g. aapl, and a name, e.g. 'Apple, inc.' """
        self.symbol = str(symbol)
        self.name = str(name)
    
    def __repr__(self):
        return "<Stock: {} -- {}>".format(self.symbol, self.name)

class Quote(Base):
    __tablename__ = 'quote'
    
    id = Column("id", Integer, primary_key=True)
    stock_id = Column('stock_id', None, ForeignKey('stock.id'))
    price = Column("price", Float)
    date = Column("date", Date)
    time = Column("time", Time)
    
    stock = relationship("Stock", backref=backref('quotes', order_by=time))
    
    def __init__(self, price, datetime, stock):
        """ Takes a stock price and time """
        self.price = float(price)
        self.date = datetime.date()
        self.time = datetime.time()
        self.stock = stock
    
    def __repr__(self):
        return "<Quote: {}={:0.2f}, at {}>".format(self.stock.symbol, self.price, self.time)

def create_tables(db_path):
    """ Create the tables for the Financials project, 'stock' and 'quote' """
    Base.metadata.create_all(engine) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
                        help="Be chatty!")
    parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", default=False,
                        help="Be quiet!")
    parser.add_argument("-c", "--create", action="store_true", dest="create", default=False,
                        help="Create tables.")
                        
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    elif args.quiet:
        logger.setLevel(logging.WARN)
    else:
        logger.setLevel(logging.INFO)
        
    if args.create:
        create_tables(os.path.join("sqlite:///", db_filename))