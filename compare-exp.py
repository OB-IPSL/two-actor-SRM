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
from modsrm import deuxexp

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


parser = argparse.ArgumentParser(description='Compare two experiments')
parser.add_argument('--noise',help='noise file',required=True)
parser.add_argument('exp1',help='Experiment 1')
parser.add_argument('exp2',help='Experiment 2')
parser.add_argument('-o',help='output file',default='out.pdf')
parser.add_argument('-k',help='keeps intermediates png files',action='store_true')
arg=parser.parse_args(argv[1:])



typeplot=2

commande="pdftk"
im=[]

exps=deuxexp(arg.exp1,arg.exp2,arg.noise,typeplot,keep=False)
im=exps.run()

if arg.o:
  nomfico=arg.o
else:
  nomfico="comp-{:}-{:}.pdf".format(arg.exp1,arg.exp2)
try:
  commande=commande+" " + nomficoo
except:
  print("commande ",commande)
  print("nomfico ",nomfico)
  exit(1)
im.save(nomfico) # , save_all=True, append_images=im[1:])


