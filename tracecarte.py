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


def indicemin(x,x0):
  imin=-1
  dmin=1.e99
  n=len(x)
  
  for i in range(0,n):
     tmp=abs(x[i]-x0)
     if tmp<dmin:
       dmin=tmp
       imin=i
  return imin


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




parser = argparse.ArgumentParser(description='Tracé des cartes Ki-Kp de 2 actors')
parser.add_argument('-l',action='store',metavar='LISTEFIC',help='fichier contenant la liste des cas')
parser.add_argument('-f',action='store',help='nom du fichier netCDF')
parser.add_argument('-s',action='store_true',help='calcul du RMS et de la moyenne. Par défaut: normes L1 et L2')
#parser.add_argument('--kp',action='store_true',help='Tracé des courbes || || = f(Kp), pour Ki = max et min') 
parser.add_argument('--ki',help='Tracé des courbes || || = f(Kp),pour les valeurs de Ki considérées')
parser.add_argument('--n1max',action='store',type=float,help='Valeur maximale de || ||_1')
parser.add_argument('--n2max',action='store',type=float,help='Valeur maximale de || ||_2')
parser.add_argument('--noise',action='store',type=float,help='temperature noise (K)')


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
  


for cas in listecas:
  print("######################### {:} #############################".format(cas))
  nomnc=cas+".nc"
  nompdf=cas+"-normes.pdf"

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
  if arg.s:
    rms=np.zeros((nkp,nki,nep))
    moy=np.zeros((nkp,nki,nep))
  else:
    norme1=np.zeros((nkp,nki,nep))
    norme2=np.zeros((nkp,nki,nep))
  fmt=4*" {:5.2f}"
  nt=tmax-tmin
  for iep in range(0,nep):
    for ip in range(0,nkp):
      for ii in range(0,nki):
        if arg.s:
          moy[ip,ii,iep]=mean(temp[tmin:tmax+1,iep,ip,ii])
          rms[ip,ii,iep]=std(temp[tmin:tmax+1,iep,ip,ii])
        else:
          norme1[ip,ii,iep]=np.linalg.norm(temp[tmin:tmax+1,iep,ip,ii]-setpoint,1)
          norme2[ip,ii,iep]=np.linalg.norm(temp[tmin:tmax+1,iep,ip,ii]-setpoint,2)

  if not arg.s:
    norme2min=norme2.min()/nt
    norme2max=norme2.max()/nt
    norme1min=norme1.min()/nt
    norme1max=norme1.max()/nt
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

    if arg.noise:
      noise_T=arg.noise
      titre=titre+" " + "# noise = {:5.2f} K".format(noise_T) 
    plt.title(titre)
    plt.xlabel('Kp')
    plt.ylabel('Ki')
    if arg.s:
      carte2d(xb,yb,rms[:,:,iep],edgecolor='black',vmin=rms.min(),vmax=rms.max())
      plt.colorbar(label='rms({:}) over years {:d}-{:d} (K)'.format(target,tmin,tmax))
    else:
      lemax=norme1max
      if arg.n1max:
        lemax=float(arg.n1max)
      carte2d(xb,yb,norme1[:,:,iep]/nt,edgecolor='black',vmin=norme1min,vmax=lemax)
      plt.colorbar(label='||{:}||_1/nyears # nyears  {:d}-{:d} (K)'.format(target,tmin,tmax))
    pp.savefig()
    plt.clf()
    
    
    titre="emission {:} target {:} ={:4.1f} K".format(em[iep],target,setpoint) 
    if arg.noise:
      noise_T=arg.noise
      titre=titre+" " + "# noise = {:5.2f} K".format(noise_T) 
                                                    
    plt.title(titre)
    
    plt.xlabel('Kp')
    plt.ylabel('Ki')


    if arg.s:
      carte2d(xb,yb,moy[:,:,iep],edgecolor='black',vmin=moy.min(),vmax=moy.max())
      plt.colorbar(label='mean({:}) over years {:d}-{:d} (K)'.format(target,tmin,tmax))
    else:
      lemax=norme2max
      if arg.n2max:
        lemax=float(arg.n2max)
      carte2d(xb,yb,norme2[:,:,iep]/nt,edgecolor='black',vmin=norme2min,vmax=lemax)
      plt.colorbar(label='||{:}||_2/nyears # years  {:d}-{:d} (K)'.format(target,tmin,tmax))

    pp.savefig()
    plt.clf()
    if arg.ki:
      try:
        listeki=[float(x) for x in arg.ki.split(",")]
        listeiki=[indicemin(ki,listeki[jj]) for jj in range(0,len(listeki))]
        print("listeki",listeki)
        print("listeiki",listeiki)
      except:
        print("incorrect ki argument : ",arg.ki)
        exit(1)
      lns=[]
      ax=plt.gca()
      ax2=ax.twinx()
      ax.set_title(titre)
      iki=20
      lns=lns+ax.plot(kp[:],norme2[:,listeiki[0],iep]/nt,color='r',label='ki={:5.1f} || ||_2'.format(listeki[0]))
      if len(listeki)>=2:
        lns=lns+ax.plot(kp[:],norme2[:,listeiki[1],iep]/nt,color='b',label='ki={:5.1f} || ||_2'.format(listeki[1]))

      if len(listeki)>=3:
        lns=lns+ax.plot(kp[:],norme2[:,listeiki[2],iep]/nt,color='g',label='ki={:5.1f} || ||_2'.format(listeki[2]))
#      lns=lns+ax.plot(kp[:],norme1[:,-1,iep]/nt,color='g',label='ki={:5.0f} || ||_1'.format(ki[-1]))
#      lns=lns+ax2.plot(kp[:],norme2[:,0,iep]/nt,color='b',label='ki=0 || ||_2')
#      lns=lns+ax2.plot(kp[:],norme2[:,-1,iep]/nt,color='m',label='ki={:5.0f} || ||_2'.format(ki[-1]))

#      lns=lns+ax2.plot(kp[:],norme2[:,0,iep]/nt,color='b',label='ki=0 || ||_2')
#      lns=lns+ax2.plot(kp[:],norme2[:,-1,iep]/nt,color='m',label='ki={:5.0f} || ||_2'.format(ki[-1]))
      labs = [l.get_label() for l in lns]
      ax.legend(lns, labs, loc=1)
      ax.set_xlabel('kp') 
#      ax.set_ylabel('|| ||_1') 
      ax2.set_ylabel('|| ||_2') 
      pp.savefig()
      plt.clf()

#    if arg.kip
#      lns=[]
#      ax=plt.gca()
#      ax2=ax.twinx()
#      ax.set_title(titre)
#
#      lns=lns+ax.plot(ki[:],norme1[0,:,iep]/nt,color='r',label='kp=0 || ||_1')
#      lns=lns+ax.plot(ki[:],norme1[-1,:,iep]/nt,color='g',label='kp={:5.0f} || ||_1'.format(kp[-1]))
#      lns=lns+ax2.plot(ki[:],norme2[0,:,iep]/nt,color='b',label='kp=0 || ||_2')
#      lns=lns+ax2.plot(ki[:],norme2[-1,:,iep]/nt,color='m',label='kp={:5.0f} || ||_2'.format(kp[-1]))
#      labs = [l.get_label() for l in lns]
#      ax.legend(lns,labs,loc=1)
#      ax.set_xlabel('ki') 
#      ax.set_ylabel('|| ||_1') 
#      ax2.set_ylabel('|| ||_2') 
#      pp.savefig()
#      plt.clf()
 
  pp.close()
