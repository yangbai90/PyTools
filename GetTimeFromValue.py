#!/usr/bin/env python3
'''
This script return the time or time step of the specific value of the input variable name
from your csv file.
So, the first column of your csv file must be time or time step. Then, the second or third...can
be whatever you like
Usage: GetTimeFromValue.py your.csv -name variablename -val 0.5 -tol 0.01
'''
import sys
import numpy as np

args,argv=len(sys.argv),str(sys.argv)

if args<4:
    sys.exit('*** Input args is too less, you should use: GetTimeFromValue.py your.csv -name variablename -val 0.5')

HasName=False;HasValue=False

VarName=''
VarVal=0.0
Tol=1.0e-2
FileName=sys.argv[1]
for i in range(args):
    if '-name' in sys.argv[i]:
        try:
            VarName=sys.argv[i+1]
            HasName=True
        except:
            sys.exit('*** Can\'t find variable name after -name')
    elif '-val' in sys.argv[i]:
        try:
            VarVal=float(sys.argv[i+1])
            HasValue=True
        except:
            sys.exit('*** Can\t find variable value after -val')
    elif '-tol' in sys.argv[i]:
        try:
            Tol=float(sys.argv[i+1])
        except:
            sys.exit('*** Can\t find tolerance value after -tol')
    else:
        continue

if (not HasName) or (not HasValue):
    sys.exit('*** Can\t find variable name or value')



##############################################################
print('*** start reading %s'%(FileName))
FoundValue=False
myfile=open(FileName,'r')
line=myfile.readline()
iInd=0
linevalue=line.split(',')
for i in range(len(linevalue)):
    iInd+=1
    if VarName in linevalue[i]:
        break
print('*** %s index is=%d'%(VarName,iInd))

line=myfile.readline()
while len(line)>1:
    linevalue=line.split(',')
    time=float(linevalue[1-1])
    if np.abs(float(linevalue[iInd-1])-VarVal)<Tol:
        print('*** %s value=%f  is found at time=%f, with tolerance=%f'%(VarName,VarVal,time,Tol))
        FoundValue=True
        break
    line=myfile.readline()
myfile.close()


if FoundValue:
    print('*** Found time !')
else:
    print('*** Nothing is found !')