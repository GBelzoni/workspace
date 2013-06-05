'''
Created on Feb 21, 2013

@author: phcostello
'''
import pandas as pd
from pandas.io.data import DataReader
from datetime import datetime

import sqlite3 
import pandas.io.sql as psql

t = datetime.now()
print datetime.date(t)

#APAC
apacSeries = { "^AORD" :   "All_Ordinaries",    
                "^SSEC" :    "Shanghai_omposite",
                "^HSI" : "HANG_SENG_INDEX",
                "BSESN" : "BSE",
                "^JKSE" : "Jakarta_Composite",    
                "^KLSE" : "KLSE_Composite",
                "^N225" : "Nikkei",
                "^NZ50" : "NZSE",
                "^STI" : "STRAITS _TIMES_INDEX",
                "^KS11" : "KOSPI",
                "^TWII" : "Taiwan_Weighted" }  

#Americas
americsSeries = { "^MERV" : "MerVal",
                 "^BVSP" : "Bovespa",   
                 "^GSPTSE" : "S&P_TSX",
                 "^MXX" : "IPC",
                 "^GSPC" : "500_Index"}

#Europe
europeSeries = {"^ATX" : "ATX",
"^FCHI"   : "CAC" ,
"^GDAXI"  :  "DAX",
"AEX.AS"  :  "AEX",
"^OSEAX"   : "OSE",
"^OMXSPI"  :  "Stockholm_General" ,
"^SSMI"  :  "Swiss_Market",
"^FTSE"  :  "FTSE_100",
"FPXAA.PR"   : "PX Index"}

#Swap keys values in dicts
apacSeries2 = { v : k for k, v in apacSeries.items()}
americsSeries2 = { v : k for k, v in americsSeries.items()}
europeSeries2 = { v : k for k, v in europeSeries.items()}


#Load SP500 symbols from file
sp500constituents = []
with open('/home/phcostello/Documents/workspace/StrategyTesterPy/sp500.csv') as fopen:
    sp500constituents = fopen.readlines()

sp500constituents = [ it.replace('\n','') for it in sp500constituents] 
if __name__ == '__main__':
    
    def importData():
        
        #Start Time
        start = datetime(2010,1,1)
        end = datetime.date(datetime.now())
        data = DataReader(sp500constituents[0], "yahoo", start, end)
        
        
        en = enumerate(sp500constituents)
        [i for i, x in en if x=='WFMI']
        
        
        sp500constituents[200:len(sp500constituents)]
        problems = []
        dataImportProblems = []
        for series in sp500constituents[485:len(sp500constituents)]:
            print series 
            try:  
                data = DataReader(series, "yahoo", start, end)
                data = data.reset_index()
            except:
                print "Can't read {}".format(series)
                dataImportProblems.append(series)
                continue
            con = sqlite3.connect("/home/phcostello/Documents/Data/FinanceData.sqlite")
            try:
                psql.write_frame( data, series, con)
                con.commit()
            except:
                print "Problems with {}".format(series)
                problems.append(series)
            finally:
                con.close()
        
        #changing tables to have date formats so RODBC driver recognizes
        #Should check that this is occuring above.
        con = sqlite3.connect("/home/phcostello/Documents/Data/FinanceData.sqlite")
        for tb in sp500constituents:
            if psql.has_table(tb, con):
                sqltxt = "SELECT * FROM {}".format(tb)
                #print sqltxt
                data = psql.read_frame(sqltxt, con)
                sqlDropTxt = 'DROP TABLE "main"."{}"'.format(tb)
                #print sqlDropTxt
                psql.execute(sqlDropTxt, con)
                con.commit()
                psql.write_frame( data, tb, con)
                con.commit()
        
        con.close()

start = datetime(2007,1,1)
end = datetime.date(datetime.now())

data = DataReader("^GSPC", "yahoo", start, end)
data = data.reset_index()
data.Date = [unicode(d) for d in data.Date]
data.Date[0]

data.head()

con = sqlite3.connect("/home/phcostello/Documents/Data/FinanceData.sqlite")
try:
    psql.write_frame( data, "SP500", con)
    con.commit()
except Exception as e:
    print "Problems with {}".format(series[0]), e
con.close()



