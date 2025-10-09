#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
#Format python datetime: %Y-%m-%dT%H:%M:%S.%f 
# fmtdate=%Y-%m-%dT%H:%M:%S.%f"
# string => datetime object:
# tt=datetime.strptime(chaine,format)
import re
import sys
import os
import numpy as np

log=False
tm=-1


#------------------------------------------------------------------------------------------
#--- SIMP START ---
# Le code jusqu'à --- SIMP END --- n'est utilisé que par le modèle
# de climat ultrasimplifié (2 hémisphères, atmosphère/océan, ....)

emipoint2jc ={"60N":0,
              "30N":1,
              "15N":2,
              "eq":3,
              "15S":4,
              "30S":5,
              "60S":6}

aremipoints =["60N",
              "30N",
              "15N",
              "eq",
              "15S",
              "30S",
              "60S"]

# var2x: fills the state vector with variables.
#         ocean temperature is not used.
#         the state vector output is used only to compute
#         emissions through the controllers.
def var2x(tsrm, tsrmnh, tsrmsh, monsoon):
  x=np.zeros(4)
  x[0]=tsrm
  x[1]=tsrmnh
  x[2]=tsrmsh
  x[3]=monsoon
  return x


target2js={"GMST":0,
           "NHST":1,
           "SHST":2,
           "monsoon":3}
js2target=["GMST","NHST","SHST","monsoon"]



type2js=target2js
# ns: size of state vector
ns=4
# nc: size of control vector
nc=len(aremipoints)
#--- SIMP END ---



#------------------------------------------------------------------------------------------

# class multipid
# members:
# - ns = size of state vector
# - nc = size of control vector 
# - xs[l] = setpoint (objective) for (l+1)-th state variable (= (l+1)-component of 
#   the state variable)
# - e:  e[l,it]=xs[l]-x[l,it] , x[i,it] being the value of the i-th component of the state
#     vector at time t[it]
# - eint: 
# - t:  t[it] = time at it-th instant
# - Kp,Ki,Kd: matrixes used to determine the control vector from the state Vector
#   Dimensions of Kp,Ki, JKd: (nc,ns)
#   (p=> proportional, i=> integral, d => derivate)
# - c[ic] = \sum_{js=0}^{m-1} poids[is] *  [ 
#                         Kp[ic,js]*e[js,it]
#                       + Ki[ic,js]}*\sum_{ict=1}^{it} 0.5*(e[js,it]+e[js,it-1])*(t[ict]-t[ict-1])
#                       + Kd[ic,js]*(e[js,it]-e[js,it-1])/(t[it]-t[it-1])]
#                        ]
#   Avec:
#   
# nt: number of times

class multipid:
  # __init__:
  # - ns = size of state vector
  # - nc = size of control vector 
  # - xs: vector of size m = setpoint 
  # - Kp,Ki,Kd,: dimension = (nc,ns)
  # - poids see supra.
  # - boundedint: bool. If true, the effect of Ki is bounded with a mechanism which tries
  #   to mimick simplePID
  # - dt time step
  #                      
  def __init__(self,ns,nc,xs,Kp,Ki,Kd,poids=[],boundedint=True,dt=1.):
    global tm
    tm=-1
    self.ns=ns
    self.nc=nc
    self.xs=xs
    self.Kp=Kp
    self.Ki=Ki
    self.Kd=Kd
    self.eint=np.zeros(self.ns)
    self.t=[]
    self.nt=0
    self.dt=dt
    self.m=self.ns
    self.n=self.nc
    self.cmin=-1.e99*np.ones(self.nc)
    self.cmax=1.e99*np.ones(self.nc)
    self.boundedint=boundedint
    if len(poids)>0:
      poids=np.array(poids)
      if poids.size!=self.ns:
        print("Erreur: nombre de variables {:d} taille du vecteur des poids {:d}".format(poids.size,
                                                                                         ns))
        exit(1)
      self.poids=poids/np.sum(poids)
    else:
      self.poids=np.ones(ns)/ns


  # setlimits: sets min and max values for output control variables
  # 
  # cmin: cmin[i] = min value for c[i]
  # cmax: cmax[i] = max value for c[i]
  # c = vector of control variables, returned by state2control 
  def setoutlimits(self,cmin,cmax):
    self.cmin=cmin*np.ones(self.nc)
    self.cmax=cmax*np.ones(self.nc)
# state2control(): computes the control variables from the state variables
#               at the times t[0],...,t[self.nt-1]
# xs:  state vector of size m
# t: current time
  def state2control(self,xs,t,isscas=-1,ikp=-1,iki=-3331,aux=None):
    global tm
    drlog=False # (iki==1 and ikp==1)
    tm=tm+1 
    self.t.append(t)
    deltaeint=np.zeros(self.ns)
    if self.nt==0:
      self.e=np.zeros([self.ns,1])
      self.eint=np.zeros(self.ns)
      self.e[:,0]=self.xs-np.array(xs)
    else:
      self.e=np.concatenate((self.e,np.reshape(self.xs-np.array(xs),(ns,1))),axis=1)
      deltaeint=self.e[:,-1]*self.dt
    self.nt=self.nt+1

   
    self.eint[:]=self.eint[:]+deltaeint[:]
    c=np.zeros(self.nc)
    e=self.e
    alpha=1.
    js0=1

    if isscas<0:
      Kp=self.Kp
      Ki=self.Ki
      Kd=self.Kd
    else:
      if (self.Kp.ndim==2):
        Kp=self.Kp
      else:
        Kp=self.Kp[:,:,isscas]

      if (self.Ki.ndim==2):
        Ki=self.Ki
      else:
        Ki=self.Ki[:,:,isscas]

      if (self.Kd.ndim==2):
        Kd=self.Kd
      else:
        Kd=self.Kd[:,:,isscas]

    for jc in range(0,self.nc):
      c[jc]=0.
      dcp=0.
      dcd=0.
      dci=0.
      for js in range(0,self.ns):
        
        drlog= ((jc==2) and (js==1))

        c[jc]=c[jc]+self.poids[js]*Kp[jc,js]*e[js,-1]+ \
                  +self.poids[js]*Ki[jc,js]*self.eint[js]
        if self.nt>=2:
          c[jc]=c[jc]+self.poids[js]*Kd[jc,js]*(e[js,-1]-e[js,-2])/(self.t[-1]-self.t[-2])
        if True: # drlog:
          dci=0.
          dcp=0.
          dcp=Kp[jc,js]*e[js,-1]*self.poids[js]
          dci=Ki[jc,js]*self.eint[js]*self.poids[js]
          somme=dci+dcp
          if somme>self.cmax[jc]:
            dcp=dcp*abs(self.cmax[jc]/somme)
            dci=dci*abs(self.cmax[jc]/somme)
          if somme<self.cmin[jc]:
            dcp=dcp*abs(self.cmax[jc]/somme)
            dci=dci*abs(self.cmax[jc]/somme)
          if Kp[jc,js]>0 and bool(aux):
            aux['dcp'].append(dcp)
          if Ki[jc,js]>0 and bool(aux):
            aux['dci'].append(dci)
          if abs(dci)>0.:
            fmt="t,e,eint,eint-e : {:3d} " + 3*(" {:12.4e}")
        if self.nt>=2:
          dcd=dcd+self.poids[js]*Kd[jc,js]*(e[js,-1]-e[js,-2])/(self.t[-1]-self.t[-2])
        else:
          dcd=0

    for js in range(0,self.ns):
      for jc in range(0,nc):

        if Ki[jc,js]>0 and self.eint[js]<self.cmin[jc]/Ki[jc,js] and tm>=50:
          print("blocage min de eint cmin={:10.2e} eint*Ki {:10.2e}".format(self.cmin[jc],
                                                                            self.eint[js]*Ki[jc,js]))
          self.eint[js]=self.cmin[jc]/Ki[jc,js]
        if Ki[jc,js]>0 and self.eint[js]>self.cmax[jc]/Ki[jc,js] and tm>=50:
          self.eint[js]=self.cmax[jc]/Ki[jc,js]
    for jc in range(0,nc):
      if c[jc]<self.cmin[jc]:
        c[jc]=self.cmin[jc]

      if c[jc]>self.cmax[jc]:
        c[jc]=self.cmax[jc]
      somme=dci+dcp
      #if c[jc]!=somme and abs(somme)>1.e-6 and bool(aux):
      #  aux['dci'][-1]=dci*abs(c[jc]/somme)
      #  aux['dcp'][-1]=dcp*abs(c[jc]/somme)
    return c

  

