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


if __name__ == '__main__':
    
    def importData():
        
#Start Time
start = datetime(2010,1,1)
end = datetime.date(datetime.now())

for series in europeSeries2.items():
    print series[1] 
    data = DataReader("^GSPC", "yahoo", start, end)
    data = data.reset_index()
    con = sqlite3.connect("/home/phcostello/Documents/Data/FinanceData.sqlite")
    try:
        psql.write_frame( data, series[0], con)
        con.commit()
    except:
        print "Problems with {}".format(series[0]), e
    con.close()



importData()
print "Done"

data = DataReader("^GSPC", "yahoo", start, end)
data = data.reset_index()
con = sqlite3.connect("/home/phcostello/Documents/Data/FinanceData.sqlite")
try:
    psql.write_frame( data, "SP5000", con)
    con.commit()
except Exception as e:
    print "Problems with {}".format(series[0]), e
con.close()



