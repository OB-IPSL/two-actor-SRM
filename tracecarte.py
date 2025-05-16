#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
#Format python datetime: %Y-%m-%dT%H:%M:%S.%f 
# fmtdate=%Y-%m-%dT%H:%M:%S.%f"
# string => datetime object:
# tt=datetime.strptime(chaine,format)

from modgraph import cellules2d,carte2d
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
trmsmin=75
trmsmax=199


f = nc4.Dataset("out-1a-kikp-nh.nc","r", format="NETCDF4")
tnhv=f.variables['T_SRM_nh']
vv=f.variables
tnh=tnhv[:,:,:,:]
t=f.variables['t'][:]
ki=vv['ki'][:]
kp=vv['kp'][:]
em=vv['emipoints'][:]
#carte2d(xb,yb,c,edgecolor='black')
(nt,nep,nkp,nki)=tnh.shape
plt.title("emission point : " + em[iep])
xb=np.zeros(nkp+1)
yb=np.zeros(nki+1)
rms=np.zeros((nkp,nki))
moy=np.zeros((nkp,nki))
for ip in range(0,nkp):
  for ii in range(0,nki):
    moy[ip,ii]=mean(tnh[trmsmin:trmsmax+1,iep,ip,ii])
    rms[ip,ii]=std(tnh[trmsmin:trmsmax+1,iep,ip,ii])
    print(moy[ip,ii],rms[ip,ii])
#print(tnh[:,0,1,1]-tnh[:,0,4,5])
xb[0]=kp[0]
xb[nkp]=kp[nkp-1]
xb[1:nkp-1]=(kp[0:nkp-2]+kp[1:nkp-1])/2.

yb[0]=ki[0]
yb[nki]=ki[nki-1]
yb[1:nki-1]=(ki[0:nki-2]+ki[1:nki-1])/2.
print("rms[0,0]=",rms[5,5])
carte2d(xb,yb,rms,edgecolor='black',vmin=rms.min(),vmax=rms.max())
plt.colorbar()

plt.show()
f.close()

