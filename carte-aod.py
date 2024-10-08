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
from socket import gethostname
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib
import matplotlib.ticker as ticker
from matplotlib import rc

from matplotlib.backend_bases import MouseButton
rc('mathtext', default='regular')


cmpt0=True # on rassemble les images à t=0 des différents cas 
delimg=False
################################################
if delimg and cmpt0:
  stderr.write('delimg et cmpt0 incompatibles\n')
  exit(1)
hostname=gethostname()
m=re.search("^spirit[0-9]",hostname)
m2=re.search("^spiritx[0-9]",hostname)
print("hostname,m,m2",hostname,m,m2)
if m:
  hote="spirit"
  datadir="/data/oboucher/S3A/"
elif m2:
  hote="spiritx"
  datadir="/data/oboucher/S3A/"
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





listecas=["ref","eq"]
tmp1=["15","30","60"]
tmp2=["S","N"]
for x in tmp1:
  for y in tmp2:
    listecas.append(x+y)

print("listecas",listecas)
liste=os.listdir(datadir)
ficemis={}

for cas in listecas:
  for xx in liste:
    r=re.match("LMDZOR-S3A-"+cas+".*",xx)
    if r:
      ficemis[cas]=xx
      break


#pp=PdfPages("cartes-{:}.pdf".format(cas))
basedir=""
#listecas=["ref"]
#listecas=["30S","30N"]
todel=[]
for cas in listecas:
  fmt=datadir+"/"+ficemis[cas]
  nomfic=fmt.format(cas)
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
  f2=open("concat.txt","w")

  i=-1
  nt=len(t)
  
  for i in range(0,nt):
    tt=t[i] 
    if cmpt0 and i>=1:
      continue
    print("{:d}/{:d}".format(i,nt))
    t1=t0+timedelta(seconds=tt)
    if cmpt0:
      titre="{:} {:} max={:7.2e} ".format(cas,t1.strftime(fmt),np.max(od))
    else:
      titre="{:} {:}".format(cas,t1.strftime(fmt))
    fig, ax = plt.subplots(1)
    #plt.title("time : {:d
    try:
      p = ax.pcolormesh(lon,lat,od[i,:,:])
    except Exception as e:
      print("pb pour le cas " + cas)
      print(e)
      continue
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title(titre)
  #  pp.savefig()
  
    nomficpng='img/{:}-{:03d}.png'.format(cas,i)
    todel.append(nomficpng)
    plt.savefig(nomficpng)
    f2.write("file '{:}'\n".format(nomficpng))
    plt.close()  

  f2.close()

  f.close()
  if not cmpt0:
    cmdfilm='ffmpeg -y -r 2 -f concat -i concat.txt -framerate 2  -c:v libx264  -pix_fmt yuv420p video/{:}.mp4'.format(cas,cas)
    print(cmdfilm.split())
    subprocess.run(cmdfilm.split())
    for xx in todel:
      try:
        os.unlink(xx)
      except Exception as e:
        print(e)
#pp.close()
#for x in var:
#  if arg.v and arg.v != var[x].name:
#    continue
#  print("variable ",x)
#  print("  name : ",var[x].name)
#  print("  dtype: ",var[x].dtype)
#  print("  dimension : ",var[x].dimensions)
#
#f.close()

liste=[]
for xx in listecas:
  liste.append("img/{:}-000.png".format(xx))
commande="montage {:}  -geometry +1+1 -tile 3x3 injections.png".format(" ".join(liste))
if cmpt0:
  subprocess.run(commande.split())
