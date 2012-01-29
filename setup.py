"""
    This file sets up my Financials project by:
        - Creating the `csv_files` subdirectory
        - Adding a cron job to download stock data 
            between 9:30AM - 4:30PM
"""

import os

if not os.path.exists("csv_files"):
    os.mkdir("csv_files")

pwd = os.getcwd()
scriptPath = os.path.join(pwd, "getCSV.py")

print "Now add the following cron job:"
print "\t00-59 09-18 * * 1-5 {0}".format(scriptPath)
print "\t(e.g. crontab -e, then copy and paste the above line)"
