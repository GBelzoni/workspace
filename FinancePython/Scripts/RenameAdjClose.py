'''
Created on Jun 14, 2013

@author: phcostello
'''

import pandas as pd
import datetime
import pandas as pd
from pandas.io.data import DataReader
from datetime import datetime
import sqlite3 
import pandas.io.sql as psql
import logging
from compiler.ast import Continue
from distutils.command.install_egg_info import safe_name
import DataDownLoader.DataDownloader as dd
from aptdaemon.lock import lists_lock


#if __name__ == '__main__':
    
conString = "/home/phcostello/Documents/Data/FinanceData.sqlite"
ddown =dd.DataDownloader(conString)
ddown.connect()
con = ddown.con

series = ddown.listSeries()

for name in series:
    sqlColumnRename = [
                   'ALTER TABLE "main"."{0}" RENAME TO "oXHFcGcd04oXHFcGcd04_{0}"'.format(name),
                   'CREATE TABLE "main"."{0}" ("Date" DATETIME,"Open" REAL,"High" REAL,"Low" REAL,"Close" REAL,"Volume" INTEGER,"Adj_Close" REAL)'.format(name), 
                   'INSERT INTO "main"."{0}" SELECT "Date","Open","High","Low","Close","Volume","Adj Close" FROM "main"."oXHFcGcd04oXHFcGcd04_{0}"'.format(name),
                   'DROP TABLE "main"."oXHFcGcd04oXHFcGcd04_{0}"'.format(name)
                   ]

    try:
        psql.execute(sqlColumnRename[0], con)
        psql.execute(sqlColumnRename[1], con)
        psql.execute(sqlColumnRename[2], con)
        psql.execute(sqlColumnRename[3], con)
    except:
        print "failed for ", name
        continue
    
    
start = datetime(2013,2,21)
end = datetime.date(datetime.now())

data = ddown.readData( u'ATI', 'yahoo', start, end)
print data
print data.columns
dlist = list(data.columns)
dlist[6]= "Adj Close"
data.columns = dlist
data.columns
ddown.writeFrameToDB(data, SeriesName='All_Ordinaries')
ddown.connect()
con = ddown.con
df2 = psql.read_frame("SELECT * FROM All_Ordinaries",con)

df2.columns == data.columns