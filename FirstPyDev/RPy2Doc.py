import rpy2.robjects as robjects

robjects.r['pi'][0]

#basic r/py vector ops
piplus2 = robjects.r('pi') + 2
piplus2.r_repr()
pi0plus2 = robjects.r('pi')[0] + 2
print(pi0plus2)

#Creating R vectors
res = robjects.StrVector(['abc', 'def'])
print(res.r_repr())
res = robjects.IntVector([1, 2, 3])
print(res.r_repr())
res = robjects.FloatVector([1.1, 2.2, 3.3])
print(res.r_repr())


#Matrices
v = robjects.FloatVector([1.1, 2.2, 3.3, 4.4, 5.5, 6.6])
m = robjects.r['matrix'](v, nrow = 2)
print(m)

#Basic function calling
rsum = robjects.r['sum']
rsum(robjects.IntVector([1,2,3]))[0]

#Help
from rpy2.robjects.packages import importr
utils = importr("utils")
help_doc = utils.help("help")
help_doc[0]

#Graphics
import rpy2.robjects as robjects

r = robjects.r

x = robjects.IntVector(range(10))
y = r.rnorm(10)

r.X11()

r.layout(r.matrix(robjects.IntVector([1,2,3,2]), nrow=2, ncol=2))
r.plot(r.runif(10), y, xlab="runif", ylab="foo/bar", col="red")
r.dev_off()

import math, datetime
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
ggplot2 = importr("ggplot2")
base = importr('base')

datasets = importr('datasets')
mtcars = datasets.mtcars

pp = ggplot2.ggplot(mtcars) + \
     ggplot2.aes_string(x='wt', y='mpg', col='factor(cyl)') + \
     ggplot2.geom_point() + \
     ggplot2.geom_smooth(ggplot2.aes_string(group = 'cyl'),
                         method = 'lm')
pp.plot()

##Linear models
from rpy2.robjects import FloatVector
from rpy2.robjects.packages import importr
stats = importr('stats')
base = importr('base')

ctl = FloatVector([4.17,5.58,5.18,6.11,4.50,4.61,5.17,4.53,5.33,5.14])
trt = FloatVector([4.81,4.17,4.41,3.59,5.87,3.83,6.03,4.89,4.32,4.69])
group = base.gl(2, 10, 20, labels = ["Ctl","Trt"])
weight = ctl + trt

robjects.globalenv["weight"] = weight
robjects.globalenv["group"] = group
lm_D9 = stats.lm("weight ~ group")
print(stats.anova(lm_D9))

# omitting the intercept
lm_D90 = stats.lm("weight ~ group - 1")
print(base.summary(lm_D90))

#PCA
import rpy2.robjects as robjects

r = robjects.r

m = r.matrix(r.rnorm(100), ncol=5)
pca = r.princomp(m)
r.plot(pca, main="Eigen values")
r.biplot(pca, main="biplot")

#PCA2
from rpy2.robjects.packages import importr

base     = importr('base')
stats    = importr('stats')
graphics = importr('graphics')

m = base.matrix(stats.rnorm(100), ncol = 5)
pca = stats.princomp(m)
graphics.plot(pca, main = "Eigen values")
stats.biplot(pca, main = "biplot")

#Creating R Vector
from rpy2.robjects import NA_Real
from rpy2.rlike.container import TaggedList
from rpy2.robjects.packages import importr

base = importr('base')

# create a numerical matrix of size 100x10 filled with NAs
m = base.matrix(NA_Real, nrow=100, ncol=10)

# fill the matrix
for row_i in xrange(1, 100+1):
    for col_i in xrange(1, 10+1):
        m.rx[TaggedList((row_i, ), (col_i, ))] = row_i + col_i * 100

"""
short demo.

"""

from rpy2.robjects.packages import importr
graphics = importr('graphics')
grdevices = importr('grDevices')
base = importr('base')
stats = importr('stats')

#One more short demo
import array

x = array.array('i', range(10))
y = stats.rnorm(10)
grdevices.dev_off()
grdevices.X11()

graphics.par(mfrow = array.array('i', [2,2]))
graphics.plot(x, y, ylab = "foo/bar", col = "red")

kwargs = {'ylab':"foo/bar", 'type':"b", 'col':"blue", 'log':"x"}
graphics.plot(x, y, **kwargs)


m = base.matrix(stats.rnorm(100), ncol=5)
pca = stats.princomp(m)
graphics.plot(pca, main="Eigen values")
stats.biplot(pca, main="biplot")

#Porting R to Python
from rpy2.robjects.vectors import DataFrame
from rpy2.robjects.packages import importr
r_base = importr('base')

#Loading data
#faithful_data = DataFrame.from_csvfile('faithful.dat', sep = " ")
datasets = importr('datasets')
faithful_data = datasets.faithful

edsummary = r_base.summary(faithful_data.rx2("eruptions"))
for k, v in edsummary.iteritems():
   print("%s: %.3f\n" %(k, v))

#Graphics
graphics = importr('graphics')
grdevices = importr('grDevices')
grdevices.dev_off()
print("Stem-and-leaf plot of Old Faithful eruption duration data")
graphics.stem(faithful_data.rx2("eruptions"))

#Histogram
grdevices = importr('grDevices')
stats = importr('stats')
grdevices.png('faithful_histogram.png', width = 733, height = 550)
grdevices.X11()
ed = faithful_data.rx2("eruptions")
graphics.hist(ed, r_base.seq(1.6, 5.2, 0.2),
              prob = True, col = "lightblue",
              main = "Old Faithful eruptions", xlab = "Eruption duration (seconds)")
graphics.lines(stats.density(ed,bw=0.1), col = "orange")
graphics.rug(ed)

from rpy2.robjects.lib import ggplot2


p = ggplot2.ggplot(faithful_data) + \
    ggplot2.aes_string(x = "eruptions") + \
    ggplot2.geom_histogram(fill = "lightblue") + \
    ggplot2.geom_density(ggplot2.aes_string(y = '..count..'), colour = "orange") + \
    ggplot2.geom_rug() + \
    ggplot2.scale_x_continuous("Eruption duration (seconds)") + \
    ggplot2.opts(title = "Old Faithful eruptions")

p.plot()

grdevices.dev_off()

#High levle interface
print(robjects.r)
import rpy2.robjects as ro
print(ro.r)

sv = ro.StrVector('ababbc')
fac = ro.FactorVector(sv)
print(fac)
fac[1]
fac.levels[1]

#Extracting python style
x = ro.r.seq(1,5)
x.names = ro.StrVector('abcde')
print(x)
x[0]

#Extracting R style
print x.rx(1)
b = ro.BoolVector((False,True,False,True,True))
print(x.rx(b))
print(x.rx(-1))

#Assignin lists done using dictionaries
x = ro.ListVector({'a': 1, 'b': 2, 'c': 3})
print x
print x[x.names.index('b')]

#NA objects
x = ro.IntVector(range(3))
x[0] = ro.NA_Integer
print x

#Check available packages
import rpy2.interactive as r
r.importr("utils")
m = r.packages.utils.available_packages()
tuple(m.colnames)

import math, datetime
import rpy2.robjects.lib.ggplot2 as ggplot2
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
base = importr('base')
stats = importr('stats')
datasets = importr('datasets')

mtcars = datasets.data.fetch('mtcars')['mtcars']
rnorm = stats.rnorm
dataf_rnorm = ro.DataFrame({'value': rnorm(300, mean=0) + rnorm(100, mean=3),
                                  'other_value': rnorm(300, mean=0) + rnorm(100, mean=3),
                                  'mean': IntVector([0, ]*300 + [3, ] * 100)})



