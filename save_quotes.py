#!/usr/bin/env python

"""
    Info on Yahoo stock API: http://www.gummy-stuff.org/Yahoo-data.htm
    
    Example:
        http://finance.yahoo.com/d/quotes.csv?s=C+AAPL+MSFT&f=snd1l1yrvjk
    
    Where:
        sndl1yrvjkm
            s = Symbol
            n = Name
            l1 = Last Trade (Price Only)
            d1 = Last Trade Date
            t1 = Last Trade Time
"""

# Standard library
import os
import re
import urllib2
import logging
import datetime
import dateutil.parser as dp
import argparse

# Third-party
import sqlalchemy as sqy
from sqlalchemy.orm import sessionmaker

# Project
import model
from model import Stock, Quote

logger = logging.getLogger(__name__)

def read_config():
    """ Read stock symbols from the 'config' file """
    
    f = open("config", "r")
    
    stocks = []
    db_file = None
    for line in f.readlines():
        key,val = line.split()
        
        if key == "stock":
            stocks.append(val)
        elif key == "db_file":
            db_file = val
    
    f.close()
    
    if db_file == None:
        raise ValueError()
    
    return dict(stocks=stocks, db_filename=db_file)
    
def main(config):
    options = "snl1d1t1"
    names = ["symbol", "name", "price", "date", "time"]
    url = "http://finance.yahoo.com/d/quotes.csv?s={0}&f={1}".format("+".join(config["stocks"]), options)

    now = datetime.datetime.now()
    try:
        data = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        logger.error("HTTP Response Error")

    Session = sessionmaker(bind=model.engine)
    session = Session()
    
    pattr = re.compile("\"([a-zA-Z]+)\",\"(.+)\",([0-9\.]+),\"([0-9/]+)\",\"([0-9apm\:]+)\"")
    
    stock_data = data.split("\n")
    for ii, stock_symbol in enumerate(config["stocks"]):
        split_data = dict(zip(names, pattr.search(stock_data[ii]).groups()))
        split_data["price"] = float(split_data["price"])
        
        logger.debug("Symbol: {}".format(split_data["symbol"]))
        logger.debug("Name: {}".format(split_data["name"]))
        logger.debug("Price: {}".format(split_data["price"]))
        logger.debug("Date: {}".format(split_data["date"]))
        logger.debug("Time: {}".format(split_data["time"]))
        
        dt = dp.parse("{} {}".format(split_data["date"], split_data["time"]))
        
        try:
            stock = session.query(Stock).filter(Stock.symbol == split_data["symbol"]).one()
            logger.info("Stock already exists in database: {}".format(stock))
        except sqy.orm.exc.NoResultFound:
            logger.info("Stock not found in database...creating: {}, {}".format(split_data["symbol"], split_data["name"]))
            stock = Stock(split_data["symbol"], split_data["name"])
            session.add(stock)
        
        try:
            quote = session.query(Quote).join(Stock)\
                           .filter(Stock.symbol == split_data["symbol"])\
                           .filter(Quote.date == dt.date())\
                           .filter(Quote.time == dt.time()).one()
            logger.info("Quote already exists in database: {}".format(quote))
        except sqy.orm.exc.NoResultFound:
            logger.info("Quote not found in database...creating: \n\t{} : {} @ {}".format(stock, split_data["price"], dt))
            quote = Quote(price=split_data["price"], datetime=dt, stock=stock)
            session.add(quote)
        
    session.commit()  

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
        logging.basicConfig(level=logging.DEBUG)
    elif args.quiet:
        logging.basicConfig(level=logging.WARN)
    else:
        logging.basicConfig(level=logging.INFO)
    
    config = read_config()
    main(config)