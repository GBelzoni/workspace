# TODO: Add comment
# 
# Author: phcostello
###############################################################################

rm(list=ls())

pima<-read.table("http://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data",header=F,sep=",")
colnames(pima)<-c("npreg","glucose","bp","triceps","insulin","bmi","diabetes","age","class")

pima$class[is.na(pima$class)]=0

pima[pima==0]=NA

pima$class=as.factor(pima$class)
levels(pima$class) = c("neg","pos")
head(pima)
summary(pima)

plot(sort(pima$bp))
hist(pima$bp)
plot(density(pima$bp,na.rm=TRUE))
plot(triceps~bmi,pima)
boxplot(diabetes~class,pima)

production<-read.table("http://www.stat.tamu.edu/~sheather/book/docs/datasets/production.txt",header=T,sep="")
plot(RunTime~RunSize)
attach(production)
plot(RunTime~RunSize)
production.lm = lm(RunTime~RunSize, data = production)
summary(production.lm)
plot(production.lm)
fitted = data.frame(production, production.lm$fitted.values, production.lm$residuals)
plot(fitted)
plot(production.lm.fitted.values~RunSize,fitted)
head(fitted)
anova(production.lm)


