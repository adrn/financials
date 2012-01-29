#!/usr/bin/env python

"""
    Info on Yahoo stock API: http://www.gummy-stuff.org/Yahoo-data.htm
    
    Example:
        http://finance.yahoo.com/d/quotes.csv?s=C+AAPL+MSFT&f=snd1l1yrvjk
    
    Where:
        sndl1yrvjkm
            s = Symbol
            n = Name
            d = Dividend / share
            l1 = Last Trade (Price Only)
            y = Dividend yield
            r = P/E ratio
            v = Volume
            j = 52-week low
            k = 52-week high
            m = Day's range
"""
import os
import urllib2
import logging
import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

projectRoot = os.path.join(os.path.expanduser("~/"), "projects", "financials")
stocks = ["C", "AAPL", "MSFT"]
options = "sndl1yrvjkm"
names = ["s","n","d","l1","y","r","v","j","k","m"]
csvRoot = os.path.join(projectRoot,"csv_files")

url = "http://finance.yahoo.com/d/quotes.csv?s={0}&f={1}".format("+".join(stocks), options)

try:
    data = urllib2.urlopen(url).read()
except urllib2.HTTPError:
    logger.error("HTTP Response Error")

now = datetime.datetime.now()
fileRoot = now.strftime("%Y-%m-%d_%H-%M.csv")
filename = os.path.join(csvRoot, fileRoot)

f = open(filename, "w")
f.write(data)
f.close()
