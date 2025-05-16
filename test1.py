#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
#Format python datetime: %Y-%m-%dT%H:%M:%S.%f 
# fmtdate=%Y-%m-%dT%H:%M:%S.%f"
# string => datetime object:
# tt=datetime.strptime(chaine,format)

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

iep=0
f = nc4.Dataset("out-1a-kikp-nh-2.nc","r", format="NETCDF4")
tnhv=f.variables['T_SRM_nh']
tnh=tnhv[:,:,:,:]
t=f.variables['t'][:]
(nt,nep,nkp,nki)=tnh.shape
for i in range(0,nkp):
  for j in range(0,nki):
    plt.plot(t,tnh[:,iep,i,j],color='blue')
plt.show()
f.close()

