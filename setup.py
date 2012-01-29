"""
    This file sets up my Financials project by:
        - Creating the `csv_files` subdirectory
        - Adding a cron job to download stock data 
            between 9:30AM - 4:30PM
"""

import os

if not os.path.exists("csv_files"):
    os.mkdir("csv_files")

homeBin = os.path.join(os.path.expanduser("~/"), "bin")
if not os.path.exists(os.path.join(homeBin)):
    os.mkdir(homeBin)

if not os.path.exists(os.path.join(homeBin, "getCSV")):
    os.link("getCSV.py", os.path.join(homeBin, "getCSV"))

if homeBin not in os.environ["PATH"].split(":"):
    f = open(os.path.join(os.path.expanduser("~/"), ".bash_profile"), "a")
    f.write("\nexport PATH=$PATH:{0}".format(os.path.normpath(homeBin)))
    f.close()

print "Now add the following cron job:"
print "\t00-59 09-18 * * 1-5 getCSV"
print "\t(e.g. crontab -e, then copy and paste the above line)"