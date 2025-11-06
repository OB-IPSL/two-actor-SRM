#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
#Format python datetime: %Y-%m-%dT%H:%M:%S.%f 
# fmtdate=%Y-%m-%dT%H:%M:%S.%f"
# string => datetime object:
# tt=datetime.strptime(chaine,format)
import re
from sys import *
import sys
import os
import subprocess
import numpy as np
from numpy import sin,cos,exp,log,tan,sqrt,mean,std,pi,arctan,arcsin,arccos
from scipy import interpolate,integrate
import phys
from os.path import isfile,isdir,islink
from ctypes import *
from struct import *
import h5py
import argparse
from datetime import *
from modsrm import generebruit

parser = argparse.ArgumentParser(description='''Generation of noise files for NH, SH and monsoon.
type and rms of noise are the same for NH and SH, but the noises generated are different
''')
parser.add_argument('--noise_type_t', type=str, default='white', 
                    choices=['white','red','pink','mixed'],
                    help='Noise type for temperature (NH and SH)')
parser.add_argument('--noise_rms_t', type=float, default=0.15, help='Temperature noise RMS (K)')
parser.add_argument('--noise_type_monsoon', type=str, default="white",
                    choices=['white','red','pink','mixed'],
                    help='Noise type for monsoon')
parser.add_argument('--noise_rms_monsoon', type=float, default=5.,help='Monsoon noise (% change)')
parser.add_argument('-n', type=int, default=200, help='number of years')
arg=parser.parse_args(argv[1:])



n=arg.n
noise_type_t=arg.noise_type_t
noise_type_monsoon=arg.noise_type_monsoon
noise_rms_t=arg.noise_rms_t
noise_rms_monsoon=arg.noise_rms_monsoon


generebruit("",
            n=n,
            noise_type_t=noise_type_t,
            noise_type_monsoon=noise_type_monsoon,
            noise_rms_t=noise_rms_t,
            noise_rms_monsoon=noise_rms_monsoon,
            file_type=1)


