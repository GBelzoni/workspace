import rpy2.robjects as robjects
#import rpy2.robjects.lib.quantmod as quantmod
from rpy2.robjects.packages import importr




quantmod = importr('quantmod')
test = 1

AORD = robjects.r('read.table("~/Documents/R/StrategyTester/Data/AORD.csv",header=T, sep=",")')
