
import pandas as pd
import os
import sys
import re
import shutil


#Paths

wd = "/home/phcostello/Documents/Data/iHub/S3_RawData"
path = wd + "/Compressed_Raw_Data/"
path2 = wd + "/Raw_Data_Rename/"
pathTmpDir = wd + "/tmpDir/"
pathConcFiles =wd + "/ConcatenatedFiles/"
os.chdir(wd)


##Get names of raw csv files

import re
#path = "/home/phcostello/Documents/Data/iHub/S3_RawData/Compressed_Raw_Data"
files = os.listdir(path)

#Create list of files ending with csv
filesRed = [ ]
for f in files:
    if f[-3:] == 'csv':
        #print f
        filesRed.append(f)

print len(files), len(filesRed)

#read mapping of files to export type, and substitute full name for label
#note file mapping type looks like column2 = {K,U,P,H,X}
fileNameExportTypeDict = {}
df2 = pd.read_csv( 'FilenameExportTypeMap.csv') #reads file mapping
rename={ 'K': 'Keywords', 'U':'Username', 'P':'Places', 'H':'Hashtags', 'X':'ToDo'}
rename['K']
df2['Stream'] = [rename[it] for it in df2['Stream']] #substitutes key for fullname using dictionary above

#create mapping fileNameWithType 
fileNameWithType = [[i[1][0], i[1][1] + "_" + i[1][0]] for i in df2.iterrows()]
print fileNameWithType[0]

#Copy raw files with new name to directory
#Defs of path above
import shutil
for f in fileNameWithType:
    shutil.copy(path + f[0],path2 + f[1])

#Read in List of fields to keep
fieldToKeep = pd.read_csv('FieldsToKeepAll.csv')
print len(fieldToKeep)




###Below is scripts to do reducing and concatenating files
#Clear tmp dir - this is needed for concatenation step
fls = os.listdir(pathTmpDir)
for f in fls:
    os.remove(pathTmpDir+f)

#Change this variable to concatenate on that query
querytype = 'Hashtags'
fileNameWithType = [[i[1][1] + "_" + i[1][0], i[1][1]] for i in df2.iterrows()]
fnt2 = pd.DataFrame(fileNameWithType)
SubstFiles = fnt2.ix[fnt2[1]==querytype]
SubstFiles
print list(SubstFiles[0])
fields = list(fieldToKeep.icol(1))
len(fields)

#Reduce to selected fields and write file with no header and row numbers
import csv
i=0

fields.append('queryType')

for f in SubstFiles[0]:
    tmpDF = pd.read_csv(path2 + f)
    tmpDF['queryType'] = querytype #Add field for querytype
    tmpDF.to_csv(pathTmpDir+'red_'+f, cols=fields, header=False,index=False, quoting=csv.QUOTE_NONNUMERIC)
    print i,f
    i+=1

print "Reducing {} done".format(querytype)

#Conncatenate Files
querytype = 'All'
outfilename = 'Conc' + querytype + '.csv'
filenames = os.listdir(pathTmpDir)
header = ','.join(fields) + '\n'

with open(pathConcFiles + outfilename, 'w') as outfile:
    outfile.write(header)
    for fname in filenames:
        with open(pathTmpDir + fname) as infile:
            for line in infile:
                #Have to remove all double quotes in file so weka can read
                line =line.replace('""','')
                outfile.write(line)

print "Concatenating {} done".format(querytype)
