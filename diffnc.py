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
from os.path import isfile,isdir
from ctypes import *
from struct import *
import h5py
import argparse
from datetime import *
from phys import tbrill,planck

import netCDF4 as nc4

parser = argparse.ArgumentParser()
parser.add_argument('fic1', type=str,  help='fichier 1',metavar='FICHIER1')
parser.add_argument('fic2', type=str,  help='fichier 2',metavar='FICHIER2')
args = parser.parse_args()

f1 = nc4.Dataset(args.fic1, "r", format="NETCDF4")
f2 = nc4.Dataset(args.fic2, "r", format="NETCDF4")
var1=f1.variables
var2=f2.variables

listevar1=list([var1[xx].name for xx in var1.keys()])
listevar2=list([var2[xx].name for xx in var2.keys()])
listevar=sorted(set(listevar1) & set(listevar2))
print(listevar)
longueur=max([len(xx) for xx in listevar])+1
fmt='{:'+"{:d}".format(longueur)+'s}' + " min={:10.2e} for t={:3d} max={:10.2e} for t={:3d} mean={:10.2e} stdev={:10.2e}"
for xx in listevar:
  if xx=="t":
    continue
  x1=var1[xx][:]
  x2=var2[xx][:]
  deltax=x2-x1
  print(fmt.format(xx,
                   deltax.min(),
                   deltax.argmin(),
                   deltax.max(),
                   deltax.argmax(),
                   np.mean(deltax),
                   np.std(deltax)))
                   
                   
f1.close()
f2.close()
