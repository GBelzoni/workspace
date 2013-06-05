'''
Created on May 2, 2013

@author: phcostello
'''

import pandas as pd
import numpy as np
from pandas.io.data import DataReader
from datetime import datetime
import sqlite3 
import pandas.io.sql as psql
import csv
import timeit



pd.set_printoptions(max_colwidth = 400)
path = "/home/phcostello/Documents/Data/iHub/S3_RawData/"
dbfile = "CrowdSourcingData.sqlite"


def showTables(con, display = True):

    cur = con.cursor()
    cur.execute("SELECT name, type FROM sqlite_master")
    tbls = pd.DataFrame(cur.fetchall())
    if(display):
        print tbls
    return tbls
    
   
def readDB(con, table, fields, startDate, endDate, DateField):  

    #Read parts of table
    
    sqlText = "select rowid, * from {0} where"\
    "(date({1}) > date('{2}') and "\
    "date({1}) < date('{3}') )".format(table,DateField,startDate,endDate)
    print sqlText
    data = psql.read_frame(sqlText, con )
    con.close()
    return data

def to_weka(data,outfile):
    
    data.to_csv(path + outfile,index=False, quoting=csv.QUOTE_NONNUMERIC)
