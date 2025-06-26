#  A n'utiliser qu'avec carte-kikp.py
# idem conf-1a-kikp-gl-3, grille modifiée
exp="kikp-14"
xs=np.zeros(4)
A={    'setpoint':0.0, 
        'emimin':0.0,
        'emimax':1000.0
        't1':0,
         't2':0,
   'stops':[],
   'target':"GMST",
   'setpoint':0,
   'Kp' : np.arange(0,50.01,0.5),
   'Ki' : np.arange(0,50.01,0.5),
#   'Kp' : np.array([0.7,0.8,0.9]),
#   'Ki' : np.array([0.5,0.6,0.7]),
   #'emipoints':['15N']
   'emipoints':['eq']
}


#################################################

geff=1.
tau_nh_sh_upper=10.
tau_nh_sh_lower=20.
Catm=7.
C0=100.
lam=1.
gamma=0.7
ndt=10

Tocean=2.
Tatm=2.
TnoSRMsh=Tatm
T0noSRMsh=Tocean
TnoSRMnh=Tatm
T0noSRMnh=Tocean
TSRMsh=Tatm
T0SRMsh=Tocean
TSRMnh=Tatm
T0SRMnh=Tocean


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
#noise_monsoon=1.  #--in % change
#--interhemispheric timescales (in years)
tau_nh_sh_upper=20.
tau_nh_sh_lower=20.

#--noise level
noise_type='red'
noise_T=0.15       #--in K
noise_monsoon=0.   #--in % change
# noisefilei: file with noise input (temperatures and moonson)
#             takes precedence over all noise parameters.
noisefilei=""
#noisefilei=""
# noisefileo: file to save noise.
noisefileo=""
eminoisestd={}
