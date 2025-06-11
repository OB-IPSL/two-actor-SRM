#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
#Format python datetime: %Y-%m-%dT%H:%M:%S.%f 
# fmtdate=%Y-%m-%dT%H:%M:%S.%f"
# string => datetime object: a
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

############################################################
couleur=["r","g","b","m","k","r","g","b","m","k"]
styleligne=["-"]*5+["--"]*5
typepoint=['+']*5+['x']*5
typepoint[3]='o'

############################################################


parser = argparse.ArgumentParser(description='Tracé de graphes à partir des données de sortie de liste-kikp.py')
parser.add_argument('-l',action='store',metavar='LISTEFIC',help='fichier contenant la liste des cas')
parser.add_argument('-f',action='store',help='nom du fichier netCDF')
parser.add_argument('-s',action='store_true',help='calcul du RMS et de la moyenne. Par défaut: normes L1 et L2')

arg=parser.parse_args(argv[1:])


if not (bool(arg.l) ^bool(arg.f)):
  stderr.write('Erreur: soit un fichier avec la liste des cas, soit le nom d''un fichier netCDF doit être fourni\n')
  exit(1)


iep=0
tmin=75
tmax=199

if arg.l:
  nomfic=arg.l
  listecas=[]
  f=open(nomfic,"r")
  for l in f:
    l=l.strip()
    if l:
      listecas.append(l)
  f.close()
elif arg.f:
  nomfic=arg.f.replace(".nc","")
  listecas=[nomfic]    
  


tmin=75
tmax=199
for cas in listecas:

  print("######################### {:} #############################".format(cas))
  nomnc=cas+".nc"
  nompdf=cas+"-temp.pdf"

  f = nc4.Dataset(nomnc,"r", format="NETCDF4")
  target=f['target'][()]
  if target=="NHST":
    tempv=f.variables['T_SRM_nh']
    temp=tempv[:,:,:]
  elif target=="SHST":
    tempv=f.variables['T_SRM_sh']
    temp=tempv[:,:,:]
  elif target=="GMST":
    tempv=f.variables['T_SRM_nh']
    tempn=tempv[:,:,:]
    tempv=f.variables['T_SRM_sh']
    temps=tempv[:,:,:]
    temp=0.5*(temps+tempn)
  setpoint=f['setpoint'][()]
  vv=f.variables
  t=f.variables['t'][:]
  titre2=f.variables['titre2'][()]
  ki=vv['ki'][:]
  kp=vv['kp'][:]
  nk=len(ki)
  em=vv['emipoints'][:]
  nep=len(em)

  emi_SRM=f.variables['emi_SRM_A'][:,:,:]
  f.close()
  #carte2d(xb,yb,c,edgecolor='black')
#  (nt,nep,nkp,nki)=temp.shape
#  xb=np.zeros(nkp+1)
#  yb=np.zeros(nki+1)
#  if arg.s:
#    rms=np.zeros((nkp,nki,nep))
#    moy=np.zeros((nkp,nki,nep))
#  else:
#    norme1=np.zeros((nkp,nki,nep))
#    norme2=np.zeros((nkp,nki,nep))
#  fmt=4*" {:5.2f}"
#  nt=tmax-tmin
#  for iep in range(0,nep):
#    for ip in range(0,nkp):
#      for ii in range(0,nki):
#        if arg.s:
#          moy[ip,ii,iep]=mean(temp[tmin:tmax+1,iep,ip,ii])
#          rms[ip,ii,iep]=std(temp[tmin:tmax+1,iep,ip,ii])
#        else:
#          norme1[ip,ii,iep]=np.linalg.norm(temp[tmin:tmax+1,iep,ip,ii]-setpoint,1)
#          norme2[ip,ii,iep]=np.linalg.norm(temp[tmin:tmax+1,iep,ip,ii]-setpoint,2)
#
#  if not arg.s:
#    norme2min=norme2.min()/nt
#    norme2max=norme2.max()/nt
#    norme1min=norme1.min()/nt
#    norme1max=norme1.max()/nt
#  #print(temp[:,0,1,1]-temp[:,0,4,5])
#  xb[0]=kp[0]
#  xb[nkp]=kp[nkp-1]
#  xb[1:nkp]=(kp[0:nkp-1]+kp[1:nkp])/2.
#  
#  yb[0]=ki[0]
#  
#  yb[nki]=ki[nki-1]
#  yb[1:nki]=(ki[0:nki-1]+ki[1:nki])/2.
#  
  pp=PdfPages(nompdf)


  for iep in range(0,nep):
    titre="emission {:} target {:} ={:4.1f} K".format(em[iep],
                                                    target,
                                                    setpoint) 
   
    titre=titre+" " + titre2
    plt.title(titre)
    plt.xlabel("time (years)")
    plt.ylabel(target+" (K)")
    for ik in range(0,nk):

      print("Kp={:7.2f} Ki={:7.2f}: ||T-Tgoal||_1={:10.2e}".format(kp[ik],
                                             ki[ik],
                                             np.linalg.norm(temp[tmin:tmax+1,iep,ik])))
      plt.plot(t,temp[:,iep,ik],
               color=couleur[ik],
               #linestyle=styleligne[ik],
               marker=typepoint[ik],
               fillstyle='none',
               markevery=10,
               label='Kp={:5.1f} Ki={:5.1f}'.format(kp[ik], ki[ik]))

    plt.legend(fontsize=8)
    pp.savefig() 
    plt.clf()            
    plt.title(titre)
    plt.xlabel("time (years)")
    plt.ylabel("emission")
    for ik in range(0,nk):
      plt.plot(t,emi_SRM[:,iep,ik],
               color=couleur[ik],
               #linestyle=styleligne[ik],
               marker=typepoint[ik],
               fillstyle='none',
               markevery=10,
               label='Kp={:5.0f} Ki={:5.0f}'.format(kp[ik], ki[ik]))

    plt.legend(fontsize=8)
    pp.savefig() 
    plt.clf()            

  pp.close()
