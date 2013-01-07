'''
Created on Dec 19, 2012

@author: phcostello
'''
import math
from scipy.stats import norm

#Prices
def ZCB( r, t0, expiry):
    
    time = expiry - t0
    price = math.exp(-r * time)
    return price

def ForwardSimple(S , K , t0 , expiry , r , dividend):
    
    time = expiry - t0
    price = math.exp(-r * time) * ( math.exp((r - dividend) * time ) * S - K )
    return price  

def BS_call(S , K , t0, expiry , r , dividend , vol):
    
    time = expiry - t0
    d1 = (math.log(S/K)+(r - dividend + 0.5*vol**2)*(time))/(vol*math.sqrt(time))
    d2 = (math.log(S/K)+(r - dividend -  0.5*vol**2)*(time))/(vol*math.sqrt(time))
    price = S*math.exp(-dividend * time)*norm.cdf(d1) - K * math.exp(-r*time) * norm.cdf(d2)
    return price  

def BS_put(S , K , t0, expiry , r , dividend , vol):
    
    time = expiry - t0
    d1 = (math.log(S/K)+(r - dividend + 0.5*vol**2)*(time))/(vol*math.sqrt(time))
    d2 = (math.log(S/K)+(r - dividend -  0.5*vol**2)*(time))/(vol*math.sqrt(time))
    price = - S*math.exp(-dividend * time)*norm.cdf(-d1) + K * math.exp(-r*time) * norm.cdf(-d2)
    return price 

def BS_Digital_call(S , K , t0, expiry , r , vol):
### Note this is delta of BS Call ###    
    time = expiry - t0
    d2 = (math.log(S/K)+(r -  0.5*vol**2)*(time))/(vol*math.sqrt(time))
    price =  math.exp(-r*time) * norm.cdf(d2)
    return price  


def BS_Digital_put(S , K , t0, expiry , r , vol):
### Note this is delta of BS Put ###    
    time = expiry - t0
    d2 = (math.log(S/K)+(r -  0.5*vol**2)*(time))/(vol*math.sqrt(time))
    price =  math.exp(-r*time) * norm.cdf(- d2)
    return price  

def BS_gamma_Euro(S , K , t0, expiry , r , vol):
    
    time = expiry - t0
    d1 = (math.log(S/K)+(r - dividend + 0.5*vol**2)*(time))/(vol*math.sqrt(time))
    gamma = 1/(2*math.pi)*math.exp(d1)/(S*vol*math.sqrt(time))
    return gamma

def BS_vega_Euro(S , K , t0, expiry , r , vol):
    
    time = expiry - t0
    d1 = (math.log(S/K)+(r - dividend + 0.5*vol**2)*(time))/(vol*math.sqrt(time))
    gamma = 1/(2*math.pi)*math.exp(d1)*S*math.sqrt(time)
    return gamma


if __name__ == '__main__':
    
    import matplotlib.pyplot as plt
    import numpy as np
    
    
    r = 0.05
    dividend = 0.0
    vol = 0.1
    S = 100.0
    t0 = 0.0
    expiry = 0.1
    K = 100.0
    
     
    print "Simple Forward:" , "%.4f" % ForwardSimple(S,K,t0,expiry,r,dividend)
    print "BS Vanilla Euro Call:" , "%.4f" % BS_call(S,K,t0,expiry,r,dividend,vol)
    print "BS Vanilla Euro Put:" , "%.4f" % BS_put(S,K,t0,expiry,r,dividend,vol)
    print "Put call parity = Call - Put - Forward:", "%.4f" % (BS_call(S,K,t0,expiry,r,dividend,vol) - BS_put(S,K,t0,expiry,r,dividend,vol) - ForwardSimple(S,K,t0,expiry,r,dividend))    
    print "Zero Coupon Bond (DF):", "%.4f" % ZCB(r, t0, expiry)
    print "BS Vanilla Euro digi Call:" , "%.4f" % BS_Digital_call(S, K, t0, expiry, r, vol)
    print "BS Vanilla Euro digi put:" , "%.4f" % BS_Digital_put(S, K, t0, expiry, r, vol)
    
    ##Deltas
    epsilon = 0.0001
    pricepldel = BS_call(S+epsilon,K,t0,expiry,r,dividend,vol)
    pricemindel = BS_call(S-epsilon,K,t0,expiry,r,dividend,vol)
    
    delta = (pricepldel - pricemindel)/(2* epsilon)
    print delta
    ##Plots
    
    underlying_range = np.arange(50,150,0.5)
    strike_range = [80,100, 120, 140]
    expiry_range = [0.01, 0.25, 0.5,0.75,1.0]
    vol_range = [0.05,0.1,0.2,0.3,0.5]
    r_range = [ 0.01, 0,03, 0.05, 0.1]
    
    #Vanilla Euro Call
    
    #underlying vs price
    fig1 = plt.figure()
    plt.subplot(1,1,1)

    for val2 in expiry_range:
        opt_price = [ BS_call(val, K, t0, val2, r, dividend, vol) for val in underlying_range]
        plt.plot(underlying_range, opt_price, label = "Expiry = " + str(val2))
    
    plt.ylabel( "Option Val")
    plt.xlabel( "underlying")
    plt.legend(loc = 'upper left')    
    plt.title("Vanilla Euro Call")
    
    #underlying vs strike
    fig2 = plt.figure()
    plt.subplot(1,1,1)

    for val2 in strike_range:
        opt_price = [ BS_call(val, val2 , t0, expiry, r, dividend, vol) for val in underlying_range]
        plt.plot(underlying_range, opt_price, label = "Strike = " + str(val2))
    
    plt.ylabel( "Option Val")
    plt.xlabel( "underlying")
    plt.legend(loc = 'upper left')    
    plt.title("Vanilla Euro Call")
    
    fig3 = plt.figure()
    plt.subplot(1,1,1)
    
    for val2 in vol_range:
        opt_price = [ BS_call(val, K , t0, expiry, r, dividend, val2) for val in underlying_range]
        plt.plot(underlying_range, opt_price, label = "Vol = " + str(val2))
    
    plt.ylabel( "Option Val")
    plt.xlabel( "underlying")
    plt.legend(loc = 'upper left')    
    plt.title("Vanilla Euro Call")
        
    #Vanilla Digital Call
    
    fig4 = plt.figure()
    plt.subplot(1,1,1)
    
    
    for val2 in expiry_range:
        opt_price = [ BS_Digital_call(val, K , t0, val2, r , vol) for val in underlying_range]
        plt.plot(underlying_range, opt_price, label = "Expiry = " + str(val2))
    
    plt.legend(loc = 'upper left')    
    plt.ylabel( "Option Val")
    plt.xlabel( "underlying")
    plt.title("Vanilla Digital Call")
    
    
    plt.show()
            