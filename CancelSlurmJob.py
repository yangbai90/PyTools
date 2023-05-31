#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script will cancel all the slurm jobs in the current folder
*Important: it must read the job id from the slurm file, in other words, you must
            have the slurm_jobid.out file
Author: Yang Bai @ 2023.05.31
"""
import os
from pathlib import Path
import subprocess
import sys

username='ybai'
if len(sys.argv)>=3:
    if '-user' in sys.argv[2-1]:
        username=sys.argv[3-1]

print('We will start to cancel all the slurm jobs for user=',username)

currentdir=os.getcwd()
scriptdir=Path(__file__).parent.resolve()

print('script dir is:',scriptdir)

def getid(instr):
    num=''
    for c in instr:
        if c.isdigit():
            num = num+c
    return num

njobs=0
for subdir, dirs, files in os.walk(scriptdir):
    for file in files:
        if 'slurm-' in file:
            print('*** start to cancel jobs in:',subdir)
            jobid=getid(file)
            njobs+=1
            cmd='scancel '+jobid
            # subprocess.run(cmd,shell=True,capture_output=True)
            subprocess.run(cmd,shell=True)
            print('***     %s (id=%d) is canceled!'%(file,int(jobid)))

print('Find %d jobs in total !'%(njobs))

