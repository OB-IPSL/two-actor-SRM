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

group = parser.add_mutually_exclusive_group()
group.add_argument('--exp-list',help='file containing the list of experiments')
group.add_argument('--exp',help='experience')

group2 = parser.add_mutually_exclusive_group()
group2.add_argument('--temp',help='Multiplicative factor only applied to Ki and Kp when the target is GMST, NHST, SHST',action='store_true')
group2.add_argument('--monsoon',help='Multiplicative factor only applied to Ki and Kp when the target is monsoon',action='store_true')
group2.add_argument('-m',help='multiplicative factor applied separately for monsoon targets and temperature targets',action='store_true')

parser.add_argument('-o',help='output file',default='out.pdf')
parser.add_argument('-k',help='keeps intermediates png files',action='store_true')
arg=parser.parse_args(argv[1:])
from modsrm import expm, expms


facteur=arg.factor
ficnoise=arg.noise

ficlisteexp=arg.exp_list
typeplot=2

if not (arg.exp or arg.exp_list):
  arg.exp="1a"

listedir=["plots-ref"] + ["plots-{:d}".format(i) for i in range(1,81)]
if ficlisteexp:
  f=open(ficlisteexp,"r")
  listeexp=[x.strip() for x in f.readlines()]
else:
  listeexp=[arg.exp]
commande="pdftk"
im=[]
for exp in listeexp:
  im.clear()
  if arg.m: 
    expmod=expms(exp,facteur,ficnoise,keep=arg.k)
    im=im+expmod.run()
  else:
    if arg.monsoon:
      expmod=expm(exp,facteur,ficnoise,keep=arg.k,target='m')
    elif arg.temp:
      expmod=expm(exp,facteur,ficnoise,keep=arg.k,target='t')
    else:
      expmod=expm(exp,facteur,ficnoise,keep=arg.k)
    im=im+expmod.run()

  nomfic="out-{:}.pdf".format(exp)
  try:
    commande=commande+" " + nomfic
  except:
    print("commande ",commande)
    print("nomfic ",nomfic)
    exit(1)
  im[0].save(nomfic, save_all=True, append_images=im[1:])
fico=arg.o
if not fico:
  fico="out.pdf"
commande=commande + " cat output " + fico
subprocess.run(commande.split())

if not arg.k:
  for xx in listedir:
    shutil.rmtree(xx,ignore_errors=True)

