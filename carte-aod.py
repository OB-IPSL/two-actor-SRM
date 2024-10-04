#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import re
from sys import *
import sys
import os
import subprocess
import numpy as np
from numpy import sin,cos,exp,log,tan,sqrt,mean,std,pi,arctan,arcsin,arccos
from scipy import interpolate,integrate
import phys
from os.path import isfile,isdir
from ctypes import *
from struct import *
import h5py
import argparse
from datetime import *
from phys import tbrill,planck
import netCDF4 as nc4

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib
import matplotlib.ticker as ticker
from matplotlib import rc

from matplotlib.backend_bases import MouseButton
rc('mathtext', default='regular')

hostname=gethostname()
m=re.search("^spiritx[0-9]?[.]",hostname)
m2=re.search("^spirit[0-9]?[.]",hostname)
if m:
  hote="spirit"
  datadir="/data/boucher/S3A/"
elif m2:
  hote="spiritx"
  datadir="/data/boucher/S3A/"
else:
  hote=hostname
  datadir="data/"



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

slat="ref"
pp=PdfPages("cartes-{:}.pdf".format(slat))
basedir=""
fmt=datadir+"/LMDZOR-S3A-{:}_19950101_20041231_1M_od550_STRAT.nc"
nomfic=fmt.format(slat)
f = nc4.Dataset(nomfic, "r")
var=f.variables
t=var['time_counter'][:]
lon=var['lon'][:]
lat=var['lat'][:]
od=var['od550_STRAT']# (t,lat,lon)

fmt="%Y-%m-%d %H:%M:%S"
t0=datetime.strptime(var['time_counter'].time_origin,
                              fmt)

nt=len(t)
i=-1
for tt in t:
  i=i+1
  if (i%10)!=0:
    continue

  print("{:d}/{:d}".format(i,nt))
  t1=t0+timedelta(seconds=tt)
  titre="{:} {:}".format(slat,t1.strftime(fmt))
  fig, ax = plt.subplots(1)
  #plt.title("time : {:d
  p = ax.pcolormesh(lon,lat,od[i,:,:])
  plt.xlabel("Longitude")
  plt.ylabel("Latitude")
  plt.title(titre)
  pp.savefig()
pp.close()
#for x in var:
#  if arg.v and arg.v != var[x].name:
#    continue
#  print("variable ",x)
#  print("  name : ",var[x].name)
#  print("  dtype: ",var[x].dtype)
#  print("  dimension : ",var[x].dimensions)
#
#f.close()
#
