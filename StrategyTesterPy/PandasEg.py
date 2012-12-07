import numpy
import scipy
import pandas
import matplotlib.pyplot as plt



ts = pandas.Series(numpy.random.randn(1000), index=pandas.DateRange('1/1/2000', periods=1000))
ts = ts.cumsum()
ts.plot()
plt.show()
pandas.rolling_mean(ts,60).plot()
plt.show()