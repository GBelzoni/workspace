'''
Created on Dec 10, 2012

@author: phcostello
'''

if __name__ == '__main__':
    pass

from QuantLib import *

effectiveDate = Date(30, 1, 1990)
terminationDate = Date(30, 1, 2000)

# The Schedule object determines the dates on which transactions occur.
s = Schedule( 
   effectiveDate, 
   terminationDate, 
   Period(Semiannual), 
   UnitedStates(UnitedStates.GovernmentBond), 
   ModifiedFollowing,
   ModifiedFollowing,
   DateGeneration.Backward,
   False
)

# FixedRateBond object's parameters
settlementDays = 3
faceAmount = 90
rate = 0.04 # this means 4%
redemption = 100.0 # this means 100% of the initial value.
todayDate = Date(24, 9, 1995) 

# Construct the object 
f = FixedRateBond( 
   settlementDays,
   faceAmount,
   s, # Schedule object
   ( rate, ), 
   ActualActual(), 
   Following, 
   redemption,
   todayDate
)

# The Bond's Yield to Maturity

print round(f.bondYield( ActualActual(), Semiannual, Semiannual ),7)

print ActualActual