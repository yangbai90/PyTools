#!/usr/bin/env python3
'''
This script can be used to clean the duplicated points (unnecessary points) after
the geometry information is ready for an image mesh

Usage: CleanDuplicateNodes.py your.geo
'''
import sys
import numpy as np
import re
args,argv=len(sys.argv),str(sys.argv)

filename=''
if args>=2:
    filename=sys.argv[1]
else:
    sys.exit('invalid input! you should run: CleanDuplicateNodes.py your.geo!!!')

print('****************************************************')
print('*** Start working on: %s'%(filename))

def SplitNumber(str):
    newstr = ''.join((ch if ch in '0123456789.-+e' else ' ') for ch in str)
    result = [float(i) for i in newstr.split()]
    return result

newfile='new'+filename

############################################
### count for the nodes num and set the active flag to 0
NodeActiveFlag=np.empty(0,dtype=np.int)
nNodes=0
AllNodeCoords=np.empty((0,3),dtype=np.float)
nodecoords=np.zeros((1,3),dtype=np.float)
with open(filename,'r') as f:
    for line in f:
        if 'Point(' in line:
            # read points
            linevalue=SplitNumber(line)
            nNodes+=1
            NodeActiveFlag=np.append(NodeActiveFlag,0)
            nodecoords[0,0]=linevalue[1];nodecoords[0,1]=linevalue[2];nodecoords[0,2]=linevalue[3]
            AllNodeCoords=np.append(AllNodeCoords,nodecoords,axis=0)
    else:
        print('*** Geo file reading Done !')
        f.close()
print('*** nodes=%d'%(nNodes))
#######################################################
### now we check if all the nodes is necesarry or not
nActiveNodes=0
with open(filename,'r') as f:
    for line in f:
        if ('Spline(' in line) or ('Line(' in line):
            linevalue=[int(s) for s in re.findall(r'\b\d+\b',line)] #use this to split integer
            for i in range(1,len(linevalue)):
                nActiveNodes+=1
                nodeid=int(linevalue[i])
                NodeActiveFlag[nodeid-1]=1
    else:
        f.close()
print('*** active nodes=%d'%(nActiveNodes))
#######################################################
### now we set the active node dofs
NodeCoords=np.zeros((nActiveNodes,3),dtype=np.float)
NodeIDMap=np.zeros(nNodes,dtype=np.int)
iInd=0
for i in range(nNodes):
    if NodeActiveFlag[i]>0:
        NodeCoords[iInd,0]=AllNodeCoords[i,0]
        NodeCoords[iInd,1]=AllNodeCoords[i,1]
        NodeCoords[iInd,2]=AllNodeCoords[i,2]
        iInd+=1
        NodeIDMap[i]=iInd
    else:
        NodeIDMap[i]=0

#######################################################
### now we can rewrite and modify the geo file
inp=open(newfile,'w')
inp.write('SetFactory("OpenCASCADE");\n')
inp.write('dx=0.2;\n')
for i in range(nActiveNodes):
    str='Point(%d)={%14.5e,%14.5e,%14.5e,dx};\n'%(i+1,NodeCoords[i,0],NodeCoords[i,1],NodeCoords[i,2])
    inp.write(str)

with open(filename,'r') as f:
    for line in f:
        if ('SetFactory("OpenCASCADE")' in line) or ('dx=0.2;' in line) or ('Point(' in line):
            continue
        elif 'Spline(' in line:
            linevalue=[int(s) for s in re.findall(r'\b\d+\b',line)]
            str='Spline(%d)={'%(linevalue[0])
            for i in range(1,len(linevalue)-1):
                totalid=linevalue[i]
                realid=NodeIDMap[totalid-1]
                str+='%d,'%(realid)
            totalid=linevalue[-1]
            realid=NodeIDMap[totalid-1]
            str+='%d};\n'%(realid)
            inp.write(str)
        elif 'Line(' in line:
            linevalue=[int(s) for s in re.findall(r'\b\d+\b',line)]
            str='Line(%d)={'%(linevalue[0])
            for i in range(1,len(linevalue)-1):
                totalid=linevalue[i]
                realid=NodeIDMap[totalid-1]
                str+='%d,'%(realid)
            totalid=linevalue[-1]
            realid=NodeIDMap[totalid-1]
            str+='%d};\n'%(realid)
            inp.write(str)
        else:
            inp.write(line)
    else:
        f.close()

inp.close()

print('*** Total nodes=%g, active nodes=%d, write result to %s'%(nNodes,nActiveNodes,newfile))

print('****************************************************')