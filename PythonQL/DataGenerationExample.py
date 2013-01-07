
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import pylab
import GenerateData as gd
reload(gd)

S0=1
mu=0.05
covariance=0.03
steps = 100
stepsize = 0.01

Normal = gd.GenerateNormalTS(S0, mu, covariance, stepsize, steps)
logNormal = gd.GenerateLogNormalTS(S0, mu, covariance, stepsize, steps)
tsLN = logNormal.get_data()
tsN = Normal.get_data()

plt.plot(tsN)
plt.plot(tsLN)
plt.show()


#generate 10k lognormal samples with mean=0 and stddev=1
samples = [random.normalvariate(0,1) for r in xrange(100)]


#demonstrate the mean and stddev are close to the target
#compute the mean of the samples
log_samples = [(sample) for sample in samples]
mu = sum(log_samples)/len(samples)
#compute the variance and standard deviation
variance = sum([(val-mu)**2 for val in log_samples])/(len(log_samples)-1)
stddev = variance**0.5

print('Mean: %.4f' % mu)
print('StdDev: %.4f' % stddev)

#Plot a histogram if matplotlib is installed
try:
    
    #hist = pylab.hist(samples,bins=100)
    #pylab.show()
    S =1
    ts=[S]
    for val in samples:
        print val
        S += S*(0.05+ 0.1*val)
        ts.append(S)       
    
    print ts
    plt.plot(ts)
    plt.show()
    
except:
    print('pylab is not available')     

def path_generate(S0,mu, vol, steps):
    samples = [random.normalvariate(0,1) for r in xrange(steps)]
    S = S0
    ts = [S]    
    for val in samples:
        S += S*(mu+ vol*val)
        ts.append(S)       
    
    return ts    

S0 =1
mu = 0.01
vol = 0.1
steps = 100

endSlice = []

#Generate lognormal stock prices
for i in range(0,10000):    
    ts = path_generate(S0, mu, vol, steps)
    endSlice.append(ts[98])
    #plt.plot(ts)


hist = pylab.hist(endSlice,bins=50)
pylab.show()
plt.show()