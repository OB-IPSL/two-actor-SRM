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


listecas=["out-1a-kikp-gl-bruitnul",
"out-1a-kikp-gl",
"out-1a-kikp-nh-bruitnul",
"out-1a-kikp-nh",
"out-1a-kikp-sh-bruitnul",
"out-1a-kikp-sh"]

for cas in listecas:
  print("######################### {:} #############################".format(cas))
  nomnc=cas+".nc"
  nompdf=cas+".pdf"

  f = nc4.Dataset(nomnc,"r", format="NETCDF4")
  target=f['target'][()]
  if target=="NHST":
    tempv=f.variables['T_SRM_nh']
    temp=tempv[:,:,:,:]
  elif target=="SHST":
    tempv=f.variables['T_SRM_sh']
    temp=tempv[:,:,:,:]
  elif target=="GMST":
    tempv=f.variables['T_SRM_nh']
    tempn=tempv[:,:,:,:]
    tempv=f.variables['T_SRM_sh']
    temps=tempv[:,:,:,:]
    temp=0.5*(temps+tempn)
  setpoint=f['setpoint'][()]
  vv=f.variables
  t=f.variables['t'][:]
  ki=vv['ki'][:]
  kp=vv['kp'][:]
  em=vv['emipoints'][:]
  f.close()
  #carte2d(xb,yb,c,edgecolor='black')
  (nt,nep,nkp,nki)=temp.shape
  xb=np.zeros(nkp+1)
  yb=np.zeros(nki+1)
  rms=np.zeros((nkp,nki,nep))
  moy=np.zeros((nkp,nki,nep))
  fmt=4*" {:5.2f}"
  print("forme",temp.shape)
  for iep in range(0,nep):
    for ip in range(0,nkp):
      for ii in range(0,nki):
        moy[ip,ii,iep]=mean(temp[trmsmin:trmsmax+1,iep,ip,ii])
        rms[ip,ii,iep]=std(temp[trmsmin:trmsmax+1,iep,ip,ii])
  #print(temp[:,0,1,1]-temp[:,0,4,5])
  xb[0]=kp[0]
  xb[nkp]=kp[nkp-1]
  xb[1:nkp]=(kp[0:nkp-1]+kp[1:nkp])/2.
  
  yb[0]=ki[0]
  
  yb[nki]=ki[nki-1]
  yb[1:nki]=(ki[0:nki-1]+ki[1:nki])/2.
  
  pp=PdfPages(nompdf)
  for iep in range(0,nep):
    titre="emission {:} target {:} ={:4.1f} K".format(em[iep],
                                                    target,
                                                    setpoint) 
    
                                                    
    plt.title(titre)
    plt.xlabel('Kp')
    plt.ylabel('Ki')
    carte2d(xb,yb,rms[:,:,iep],edgecolor='black',vmin=rms.min(),vmax=rms.max())
    plt.colorbar(label='rms({:}) over years {:d}-{:d} (K)'.format(target,trmsmin,trmsmax))
    pp.savefig()
    plt.clf()
    
    
    titre="emission {:} target {:} ={:4.1f} K".format(em[iep],
                                                    target,
                                                    setpoint) 
    
                                                    
    plt.title(titre)
    
    plt.xlabel('Kp')
    plt.ylabel('Ki')
    carte2d(xb,yb,moy[:,:,iep],edgecolor='black',vmin=moy.min(),vmax=moy.max())
    
    plt.colorbar(label='mean({:}) over years {:d}-{:d} (K)'.format(target,trmsmin,trmsmax))
    pp.savefig()
    plt.clf()
  
  pp.close()
