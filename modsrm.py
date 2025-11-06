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
from colorednoise import powerlaw_psd_gaussian


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



def generebruit(nomfic,
                n,
                noise_rms_t,
                noise_rms_monsoon,
                noise_type_t,
                noise_type_monsoon,
                file_type=1,
                file_o):

  if not nomfic:
    nomfic="bruit-{:}-{:}-{:5.2f}-{:5.2f}.txt".format(noise_type_t,
                                                    noise_type_monsoon,
                                                    noise_rms_t,
                                                    noise_rms_monsoon).replace(' ','')
  if file_type!=1:
    stderr.write('value of file_type not supported')
    exit(2)
  f = open(nomfic,"w")
  f.write('''noise_t: {:} rms={:5.2f} K # noise_monsoon: {:} rms={:5.2f}
Column 1: year
Column 2: Tsh_noise (K)
Column 3: Tnh_noise (K)
Column 4: monsoon noise (K)
'''.format(noise_type_t,
           noise_rms_t,
           noise_type_monsoon,
           noise_rms_monsoon))

  if noise_type_t=='mixed' :
    noise_white=noise_rms_t*powerlaw_psd_gaussian(0,n)
    noise_red=noise_rms_t*powerlaw_psd_gaussian(2,n)
    noise_mixed=0.5*(noise_white+noise_red)
    noise_nh=noise_rms_t*(noise_mixed/std(noise_mixed))


    noise_white=noise_rms_t*powerlaw_psd_gaussian(0,n)
    noise_red=noise_rms_t*powerlaw_psd_gaussian(2,n)
    noise_mixed=0.5*(noise_white+noise_red)
    noise_sh=noise_rms_t*(noise_mixed/std(noise_mixed))

  else:
    if (noise_type_t=='red') or  (noise_type_t=='brown'):
      noise_exp=2
    elif noise_type_t=='pink':
      noise_exp=1
    elif noise_type_t=='white':
      noise_exp=0
    noise_nh=noise_rms_t*powerlaw_psd_gaussian(noise_exp,n)
    noise_sh=noise_rms_t*powerlaw_psd_gaussian(noise_exp,n)
  if noise_type_monsoon=='mixed' :
    noise_white=noise_rms_monsoon*powerlaw_psd_gaussian(0,n)
    noise_red=noise_rms_monsoon*powerlaw_psd_gaussian(2,n)
    noise_mixed=0.5*(noise_white+noise_red)
    noise_monsoon=noise_rms_monsoon*(noise_mixed/std(noise_mixed))
  else:
    if (noise_type_monsoon=='red') or  (noise_type_monsoon=='brown'):
      noise_exp=2
    elif noise_type_monsoon=='pink':
      noise_exp=1
    elif noise_type_monsoon=='white':
      noise_exp=0
    noise_monsoon=noise_rms_monsoon*powerlaw_psd_gaussian(noise_exp,n)
   
  for i in range(0,n):
    f.write('{:d} {:22.14e} {:22.14e} {:22.14e}\n'.format(i,
                                                          noise_sh[i],
                                                          noise_nh[i],
                                                          noise_monsoon[i]))
  f.close()

