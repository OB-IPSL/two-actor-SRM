exp="1a-18-kp5"
xs=np.zeros(4)
A={    
       'emimin':0.0,
       'emimax':20.0,
       't1':0,
        't2':0,
   'stops':[],
   'targets':{"GMST":0.,},
   'poids':{"GMST":1.},
'dicKp':{'NHST': {},
       'SHST': {},
         'GMST': {'eq':5.},
       'monsoon' : {}},
'dicKi':{'NHST':{},
       'SHST': {},
         'GMST': {'eq':4.},
       'monsoon' : {}},
}
Tocean=0.
Tatm=0.
TnoSRMsh=Tatm
T0noSRMsh=Tocean
TnoSRMnh=Tatm
T0noSRMnh=Tocean
TSRMsh=Tatm
T0SRMsh=Tocean
TSRMnh=Tatm
T0SRMnh=Tocean


#################################################

geff=1.
tau_nh_sh_upper=10.
tau_nh_sh_lower=20.
Catm=7.
C0=100.
lam=1.
gamma=0.7
ndt=10

B=False
C=False
D=False

for Actor in [A,B,C,D]:
  if not Actor:
    continue
  liste=[]
  for clef1 in ['dicKp','dicKi','dicKd']:
    if not (clef1 in Actor.keys()):
      continue
    dic=Actor[clef1]
    for target in dic:
      for emip in dic[target]:
        if not emip in liste:
          liste.append(emip)
  
  Actor['aremipoints2']=liste


#--directory for plots
dirout='plots/'
#--show plots while running
pltshow=False
#--if non empty, output PDF file.


#--period 
t0=0 ; t5=200
#--volcano
volcano=True
#--max GHG forcing
fmax=4.0
f=np.ones((t5))*fmax
#--noise level

noise_type='red'
noise_T=0.       #--in K
noise_monsoon=5.   #--in % change
#noise_monsoon=1.  #--in % change
#--interhemispheric timescales (in years)
tau_nh_sh_upper=20.
tau_nh_sh_lower=20.



# noisefilei: file with noise input (temperatures and moonson)
#             takes precedence over all noise parameters.
noisefilei=""
#noisefilei=""
# noisefileo: file to save noise.
noisefileo=""
eminoisestd={}
