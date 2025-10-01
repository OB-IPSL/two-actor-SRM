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

import PIL
from PIL import Image,ImageFont
from PIL import ImageDraw
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

def concatimages(images,typeplot=1):
  width=images[0].width
  height=0
  width=0
  if typeplot==1:
    for im in images:
      height=height+im.height
  else:
    for im in images:
      width=width+im.width

  dst=Image.new("RGB",(width,images[0].height))
  dst.paste(images[0], (0, 0))
  if typeplot==1:
    y=images[0].height
  else:
    x=images[0].width
  for im in images[1:]:
    if typeplot==1:
      dst.paste(im,(0,y))
      y=y+im.height
    else:
      dst.paste(im,(x,0))
      x=x+im.width
  return dst


