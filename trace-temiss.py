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

import netCDF4 as nc4

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib
import matplotlib.ticker as ticker
from matplotlib import rc

from matplotlib.backend_bases import MouseButton
rc('mathtext', default='regular')

# position de la legende (loc=)
# 2  9 1
# 6 10 7
# 3  8 4
# Mots clefs pour plot:
# - color ='#XXXXXX" (couleur en hexa)
# - lw=1.5 : épaisseur des lignes
# - mew=1.5 : épaisseur des traits de symboles (x, +, ...)
# - markersize=10: taille des symboles
# - linestyle: type de la ligne
# - marker: type de symbole 
# - fillstyle: remplissage du symbole

parser = argparse.ArgumentParser(description='Tracé des cartes Ki-Kp de 2 actors')
parser.add_argument('f',action='store',help='nom du fichier netCDF')

arg=parser.parse_args(argv[1:])



f = nc4.Dataset(arg.f,"r", format="NETCDF4")
tshv=f.variables['T_SRM_nh']
tsh=tshv[:]

tnhv=f.variables['T_SRM_nh']
tnh=tnhv[:]

emiv=f.variables['emi_SRM_A_eq']
emi=emiv[:]


tv=f.variables['t']
t=tv[:]

tg=(tsh+tnh)/2.
ax=plt.gca()
ax2=plt.twinx()
ax.set_ylabel('GMST (K)')
ax2.set_ylabel('emission (eq)')
ax.set_xlabel('time (years)')
lns1=ax.plot(t,tg,'r-x',label='GMST')
lns2 =ax2.plot(t,emi,'g-+',label='emi_eq')
lns=lns1+lns2
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=3)
plt.xlim(50,60)



