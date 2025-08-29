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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib
import matplotlib.ticker as ticker
from matplotlib import rc

from matplotlib.backend_bases import MouseButton
rc('mathtext', default='regular')

def concatficimages(ficimages,outfile):
  images=[]
  for xx in ficimages:
    images.append(Image.open(xx))
  width=images[0].width
  height=0
  for im in images:
    height=height+im.height
  print("height=",height)
  dst=Image.new("RGB",(images[0].width,height))
  dst.paste(images[0], (0, 0))
  y=images[0].height
  for im in images[1:]:
    print("y=",y)
    dst.paste(im,(0,y))
    y=y+im.height
  dst.save(outfile)

def concatimages(images):
  width=images[0].width
  height=0
  for im in images:
    height=height+im.height
  print("height=",height)
  dst=Image.new("RGB",(images[0].width,height))
  dst.paste(images[0], (0, 0))
  y=images[0].height
  for im in images[1:]:
    print("y=",y)
    dst.paste(im,(0,y))
    y=y+im.height
  return dst


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

#ficimages=["plots-ref/experiment4a.png","plots-kix2/experiment4a.png"]
#images = [Image.open(x) for x in ficimages]
#widths, heights = zip(*(i.size for i in images))
#dx=widths[0]
#dy=heights[0]
#
#imblanc = PIL.Image.new('RGB',(dx,100),"rgb(255,255,255)")
#im2=imblanc.copy()
#font1 = ImageFont.truetype("gentium/Gentium-R.ttf",40)
#im2d=ImageDraw.Draw(im2)
#im2d.text((10,20),"aaa",fill=(255,0,0),font=font1)
#im2.save("aaa.png")
#exit(2)
#print(widths)
#print(heights)
#exit(2)





#ficimages=["plots-1/experiment4a.png","plots-ref/experiment4a.png"]
#concatimages(ficimages,"out.png")
#im1 = PIL.Image.open("plots-ref/experiment4a.png").convert("RGB")
#im2 = PIL.Image.open("plots-1/experiment4a.png").convert("RGB")
#images = [im1,im2]
#images[0].save("out.pdf", save_all=True, append_images=images[1:])
