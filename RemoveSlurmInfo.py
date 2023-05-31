#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script delete all the slurm job's outputs (slurm-xxx.out and job.errorxxx)
Author: Yang Bai @ 2023.05.31
"""
import os
from pathlib import Path
import subprocess
import sys

scriptdir=Path(__file__).parent.resolve()

print('Remove script dir is:',scriptdir)

nfiles=0
for subdir, dirs, files in os.walk(scriptdir):
    for file in files:
        if 'slurm-' in file or 'job.err.' in file:
            removepath=subdir+'/'+file
            os.remove(removepath)
            nfiles+=1
            print('*** %s has been removed !'%(file))

print('%d files have been removed !'%(nfiles))

