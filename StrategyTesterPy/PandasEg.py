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

df = pandas.DataFrame(ts)

print df
len(df)
df.index[1]

df.ix[1]
df2 = pandas.DataFrame(columns = ( 'Time', 'Value', 'Signal'))
df= pandas.DataFrame({'a':[1],'b':[1], 'c':[1]})
row = pandas.DataFrame( {'Time':2,'Value':2, 'Signal':2})
df2.append(row, ignore_index=True)
