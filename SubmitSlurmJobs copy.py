#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script will submit all the slurm jobs in the current folder
*Important: it must read the job.sh file
Author: Yang Bai @ 2023.05.31
"""
import os
from pathlib import Path
import subprocess
import sys

currentdir=os.getcwd()
scriptdir=Path(__file__).parent.resolve()

print('Start to submit job.sh in :',scriptdir)

njobs=0
for subdir, dirs, files in os.walk(scriptdir):
    for file in files:
        if 'job.sh' in file:
            print('*** start to submit job in:',subdir)
            os.chdir(subdir)
            cmd='sbatch job.sh'
            subprocess.run(cmd,shell=True)
            njobs+=1

print('Submit %d jobs in total !'%(njobs))
