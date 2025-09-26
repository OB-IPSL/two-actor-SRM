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
import shutil

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

import PIL
from PIL import Image,ImageFont
from PIL import ImageDraw
from modpil import concatimages
from experiments import set_experiment


parser = argparse.ArgumentParser(description='Study the effect of multiplying Kp and Ki')
parser.add_argument('--factor',type=float,help='multiplicative factor for Ki and Kpw',
                    required=True)
parser.add_argument('--noise',help='noise file',required=True)
parser.add_argument('-m',help='multiplicative factor applied separately for monsoon targets and temperature targets',action='store_true')
parser.add_argument('--exp-list',help='file containing the list of experiments',
                    default="liste-exp.txt")

parser.add_argument('-o',help='output file',default='out.pdf')
parser.add_argument('-k',help='keeps intermediates png files',action='store_true')
arg=parser.parse_args(argv[1:])



facteur=arg.factor
ficnoise=arg.noise
ficlisteexp=arg.exp_list
typeplot=2

# expms: comme expm, mais on garde la possibilité d'avoir des valeurs différentes
# pour les Ki température et les Ki mousson (si l'expérience) 
class expms:
  def __init__(self,exp,facteur,ficnoise):
    self.facteur=facteur
    self.exp=exp
# self.monsoon: vrai si la cible d'au moins un acteur est 'monsoon'
# self.temperature: vrai si la cible d'au moins un acteur est 'GMST','SHST' ou 'NHST'
    self.monsoon=False
    self.temperature=False
    actors=set_experiment(exp)
    for acteur in actors:
      if actors[acteur]['target']=='monsoon':
         self.monsoon=True
      elif actors[acteur]['target'] in ('GMST','NHST','SHST'):  
         self.temperature=True
    #print("exp,temp,monsoon",exp,self.temperature,self.monsoon)
  def run(self):
    global listedir
    # ckits: cki coefficient multiplicatif de Ki opur la température
    # ckims: cki coefficient multiplicatif de Ki opur la mousson
    ckits=[]
    ckpts=[]
    ckims=[]
    ckpms=[]
    if self.monsoon ^self.temperature:
      listedir=["plots-ref"] + ["plots-{:d}".format(i) for i in range(1,5)]
      ckps=[1.,self.facteur,1./self.facteur,1.,1.,1.]
      ckis=[1.,1.,1,self.facteur,1./self.facteur]
      im=[]
      ficimages=[]
      nfac=len(ckits)
      for i in range(0,5):
        titre=""
        cki=ckis[i]
        ckp=ckps[i]
        titre="EXP: {:} ".format(exp)
        if i==0:
          titre=titre+ " REFERENCE"
        else:
          if abs(ckp-1)>1.e-3:
            titre=titre+"ckp={:5.1f}".format(ckp)
          if abs(cki-1)>1.e-3:
            titre=titre+"cki={:5.1f}".format(cki)
        if isdir("plots") or islink("plots"):
          os.unlink("plots")
        if isdir(listedir[i]):
          shutil.rmtree(listedir[i],ignore_errors=True)
        os.mkdir(listedir[i])
        os.symlink(listedir[i],"plots")
        commande="./main.py --exp {:} --cki {:5.1f} --ckp {:5.1f} --type-plot {:d} --load-noise {:} --app-title ".format(exp,cki,ckp,typeplot,ficnoise)
        arcomm=commande.split()
        arcomm.append(titre)
        subprocess.run(arcomm)
        ficimages.append("{:}/experiment{:}.png".format(listedir[i],exp))
      im=[Image.open(ficimages[i]) for i in range(0,5)]
    else:
      listedir=["plots-ref"] + ["plots-{:d}".format(i) for i in range(1,81)]
      ficimages=[]
      i=-1
      for ckpt in (1.,self.facteur,1./self.facteur):
        for ckit in (1.,self.facteur,1./self.facteur):
          for ckpm in (1.,self.facteur,1./self.facteur):
            for ckim in (1.,self.facteur,1./self.facteur):
               i=i+1
               titre=""
               print("i={:2d} ckpt ckit ckpm ckim {:4.1f} {:4.1f} {:4.1f} {:4.1f}".format(i,
                                                                                         ckpt,
                                                                                         ckit,
                                                                                         ckpm,
                                                                                         ckim))
               titre="EXP: {:} ".format(exp)
               if i==0:
                 titre=titre+ " REFERENCE"
               else:
                 if abs(ckpt-1)>1.e-3:
                   titre=titre+" ckpt={:5.1f}".format(ckpt)
                 if abs(ckit-1)>1.e-3:
                   titre=titre+" ckit={:5.1f}".format(ckit)
                 if abs(ckpm-1)>1.e-3:
                   titre=titre+" ckpm={:5.1f}".format(ckpm)
                 if abs(ckim-1)>1.e-3:
                   titre=titre+" ckim={:5.1f}".format(ckim)
               if islink("plots"):
                 os.unlink("plots")
               elif isdir("plots"):
                 shutil.rmtree(listedir[i],ignore_errors=True)
                
                 print("i = ",i," point 2")
               if islink(listedir[i]):
                 os.unlink(listedir[i])
               elif isdir(listedir[i]):
                 shutil.rmtree(listedir[i],ignore_errors=True)
               os.mkdir(listedir[i])
               os.symlink(listedir[i],"plots")
               commande="./main.py --exp {:} --cki {:5.1f} --ckp {:5.1f} --ckim {:5.1f} --ckpm {:5.1f} --type-plot {:d} --load-noise {:} --app-title ".format(exp,ckit,ckpt,ckim,ckpm,typeplot,ficnoise)
               arcomm=commande.split()
               arcomm.append(titre)
               subprocess.run(arcomm)
               ficimages.append("{:}/experiment{:}.png".format(listedir[i],exp))
               os.unlink("{:}/scenario{:}.png".format(listedir[i],exp))
               os.unlink("{:}/test{:}.png".format(listedir[i],exp))
 
      im=[Image.open(ficimages[i]) for i in range(0,81)]




    if typeplot>=2:
      imc=[]
      for i in range(1,81):  
        imc.append(concatimages([im[0],im[i]],typeplot=typeplot))
    #    imc[-1].save("im{:d}.png".format(i))   
      return imc
 
class expm:
  def __init__(self,exp,facteur,ficnoise):
    self.facteur=facteur
    self.exp=exp
  def run(self):
    print("a")
    global listedir
    ckis=[1.,1.,1,self.facteur,1./self.facteur]
    ckps=[1.,self.facteur,1./self.facteur,1.,1.,1.]

    im=[]
    ficimages=[]
    for i in range(0,5):
      titre=""
      cki=ckis[i]
      ckp=ckps[i]
      titre="EXP: {:} ".format(exp)
      if i==0:
        titre=titre+ " REFERENCE"
      else:
        if abs(ckp-1)>1.e-3:
          titre=titre+"ckp={:5.1f}".format(ckp)
        if abs(cki-1)>1.e-3:
          titre=titre+"cki={:5.1f}".format(cki)
      if isdir("plots") or islink("plots"):
        os.unlink("plots")
      if isdir(listedir[i]):
        shutil.rmtree(listedir[i],ignore_errors=True)
      os.mkdir(listedir[i])
      os.symlink(listedir[i],"plots")
      commande="./main.py --exp {:} --cki {:5.1f} --ckp {:5.1f} --type-plot {:d} --load-noise {:} --app-title ".format(exp,cki,ckp,typeplot,ficnoise)
      arcomm=commande.split()
      arcomm.append(titre)
      subprocess.run(arcomm)
      ficimages.append("{:}/experiment{:}.png".format(listedir[i],exp))
    im=[Image.open(ficimages[i]) for i in range(0,5)]
    if typeplot==1:
      im1=concatimages([im[0],im[1],im[2]],typeplot=typeplot)
      im2=concatimages([im[0],im[3],im[4]],typeplot=typeplot)
      return [im1,im2]
    elif typeplot>=2:
      im1=concatimages([im[0],im[1]],typeplot=typeplot)
      im2=concatimages([im[0],im[2]],typeplot=typeplot)
      im3=concatimages([im[0],im[3]],typeplot=typeplot)
      im4=concatimages([im[0],im[4]],typeplot=typeplot)

      #print("im4.size",im4.width,im4.height)
      im1.save("im1.png")
      im2.save("im2.png")
      im3.save("im3.png")
      im4.save("im4.png")
      return [im1,im2,im3,im4]
  
listedir=["plots-ref"] + ["plots-{:d}".format(i) for i in range(1,81)]
for xx in listedir:
  shutil.rmtree(xx,ignore_errors=True)
f=open(ficlisteexp,"r")
listeexp=[x.strip() for x in f.readlines()]
im=[]
for exp in listeexp:
  if arg.m: 
    expmod=expms(exp,facteur,ficnoise)
    im=im+expmod.run()
  else:
    expmod=expm(exp,facteur,ficnoise)
    im=im+expmod.run()

im[0].save(arg.o, save_all=True, append_images=im[1:])
if not arg.k:
  for xx in listedir:
    shutil.rmtree(xx,ignore_errors=True)

