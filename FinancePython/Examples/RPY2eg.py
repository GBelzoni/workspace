import rpy2.robjects as ro

from rpy2.robjects.packages import importr

import rpy2.rinterface as ri
ri.set_initoptions(('rpy2', '--verbose', '--no-save'))
ri.initr()

graphics = importr('graphics')
grdevices = importr('grDevices')
base = importr('base')
stats = importr('stats')
zoo = importr('zoo')

#Need to add params to importr as xts and quantmod have conflicts
xts = importr("xts", robject_translations = {".subset.xts": "_subset_xts2",                                            "to.period": "to_period2"})
quantmod = importr('quantmod', robject_translations = {"skeleton.TA": "skeleton_TA2"})

AORD = ro.r('read.table("~/Documents/R/StrategyTester/Data/AORD.csv",header=T, sep=",")')

#WIP - using quantmod, zoo, xts in Python.
#Create Zoo object
#indexZoo = ro.r.rownames(AORD)
AORD = zoo.as_zoo(AORD)
AORD = xts.as_xts(AORD)

#Create MA zoo object
#Creating EMA using quantmod
chartData = AORD#.rx['2008-02::2008-08']
quantmod.chartSeries(chartData, theme="white")
EMA1=quantmod.addEMA(n=10,col=2)
EMA1Vals=EMA1.do_slot("TA.values")
EMA2=quantmod.addEMA(n=20)
EMA2Vals=EMA2.do_slot("TA.values")
grdevices.dev_off()
zoo.index(AORD)

#Adding MA to Data object
Series1 = xts.as_xts(zoo.zoo(EMA1Vals,order_by=zoo.index(chartData)))
type(Series1)
zoo.plot_zoo(Series1)
zoo.str_zoo(Series1)

Series2 = xts.as_xts(zoo(EMA2Vals,order_by=zoo.index(chartData)))#;colnames(Series2)="MAl"
chartData = xts.cbind_xts(chartData,Series1,Series2 )
ro.r.head(chartData,2)



namess = list(ro.r.colnames(AORD))
print namess
namess[1]