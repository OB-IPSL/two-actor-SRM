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
import matplotlib.pyplot as plt
import numpy as np
import colorednoise as cn
from simple_pid import PID
import random
from myclim import clim_sh_nh,  emi2aod, emi2rf, Monsoon, Monsoon_IPSL
from matplotlib import rc
#--set time profiles of climate noise

parser = argparse.ArgumentParser(description='Génération de bruit dont la densité spectrale de puissance suit une loi en 1/f^n')
parser.add_argument('-n',help='Densité spectrale de puissance en 1/f^n (f = fréquence). Default: 0 (bruit blanc)',type=int, default=0)

parser.add_argument('-c',help='Coefficient multiplicatif du bruit. Egal RMS pour le bruit blanc. Valeur par défaut: 1.'
                         ,type=float
                         ,default=1.)
parser.add_argument('-o',help='outputfile. If not defined, stdout is used')
parser.add_argument('-s',type=int,default=100,help='nombre de valeurs. Par défaut: 10')


arg=parser.parse_args(argv[1:])

if arg.o:
  fo=open(arg.o,"w")
else:
  fo=stdout
y=cn.powerlaw_psd_gaussian(arg.n,arg.s)*arg.c
for yy in y:
  fo.write('{:22.14e}\n'.format(yy))
if arg.o:
  fo.close

