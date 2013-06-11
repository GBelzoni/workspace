import sys, os
path = "/home/phcostello/Documents/workspace/TestBoostPython/Debug/"
#os.environ['LD_LIBARY_PATH'] = "${workspace_loc}/JoshiLibrary/Debug"
os.environ['LD_LIBARY_PATH'] = "${workspace_loc}/TestBoostPython/Debug"

Spot = 50.0
Strike = 60.0   
r=0.0
d=0.0
Vol =0.2
Expiry = 1.0
import CurveRatesPy
from CurveRatesPy import *


#print greet()
#print BlackScholesCall( Spot, Strike, r, d, Vol, Expiry)

#Initialise curve - LinearZeroes Bootstrapper
curve = CurveRatesPy.CurveBootStrapLZ()

### FIT CURVE FROM DEPOS
#Initialize Depos
depoRates = [0.03,0.04,0.04]
depoExpiries = [1,2,3]
depoInfo = zip(depoRates,depoExpiries)

depos= [ CurveRatesPy.DepoInstrument( info[0],info[1] ) for info in depoInfo ]

#Build curve from DepositRateHelper
for d in depos:
    curve.addInstrument(d)

curve.fit()

#Query curve for swap rates
rates = [ curve.getRate( 0.5, expiry, 2, 2 ) for expiry in depoExpiries ]

for it in zip(depoExpiries,rates):
    print "Expiry: ", it[0], " Rate: ", round( it[1],4)
    

#Now check zeroes are piecwise linearly interpolated    
times = [0.05*i for i in range(0,8)]

dfs = [curve.get_DF_instrument(t) for t in times]

zeroes = [df.getCcr() for df in dfs]

#Plot zeroes vs dfs






###FIT curve from zero rates
###Check that it gives linear curves
#
##zero Rates
#expiries = [1.0,2.0,3.0]
#zeroes = [0.03,0.04,0.07]
#zeroInfo = zip(zeroes, expiries)
#
##Create DF objects
#Dfs = [ InstrumentDF().fromCcr(it[0],it[1]) for it in zeroInfo]

#Get simple rates

#Create Depos

#Add to curve and fit

#Get zeroes for range of dates

#Plot




#BUild curve from FRAS

#BUild curve from Swap

