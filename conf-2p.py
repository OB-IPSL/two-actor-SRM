exp="2p"
xs=np.zeros(4)
emimaxl=20.
emipoint1='60N'
emipoint2='60S'
A={    'emimin':0.0,'emimax':emimaxl,'emipoints':[emipoint1],'t1':50,'t2':70,'stops':[],
    'targets':{"NHST":0.,
         "SHST":3.},
   'poids':{"NHST":1.,
         "SHST":1.},
   'dicKp':{'NHST': {emipoint1:0.8},
       'SHST': {emipoint2:0.8},
       'GMST': {},
       'monsoon' : {}},
   'dicKi':{'NHST': {emipoint1:0.6},
       'SHST': {emipoint2:0.6},
       'GMST': {},
       'monsoon' : {}},
   'dicKd':{'NHST': {},
       'SHST': {},
       'GMST': {},
       'monsoon' : {}}
}
aremipoints2 =[]
for clef1 in ['dicKp','dicKi','dicKd']:
  dic=A[clef1]
  for tt in dic:
    for emip in dic[tt]:
      if not emip in aremipoints2:
        aremipoints2.append(emip)
print("aremipoints2",aremipoints2)


# Paramètres du modèle physique




#################################################
# output parameters
# outnc: output netCDF file
# Default value: out-EXP.nc EXP = value of exp parameter
#outnc="out-2m.nc"
# outpdf: output PDF file
# Default value: out-EXP.pdf EXP = value of exp parameter
#outpdf="sortie-2m}.pdf".format(exp)

#--directory for plots
dirout='plots/'
#--show plots while running
pltshow=False
#--if non empty, output PDF file.

#--period 
t0=0 ; t5=200
#--volcano
volcano=False

#--max GHG forcing
# --fmax: max value for GHG forcing (Wm-2)
# either f, either fmax should be defined here
fmax=8.0


#f=np.zeros((t5))
#f[0:100]=np.linspace(0.,fmax,100)
#f[100:150]=fmax
#f[150:]=np.linspace(fmax,3*fmax/4,50)
## -transient decrease in forcing if volcanic eruption
#if volcano:
#   f[125]+=-2.0
#   f[126]+=-1.0
#

#noise_monsoon=1.  #--in % change
#--interhemispheric timescales (in years)
# 1.e9: valeur irréaliste destinée à découpler thermiquement les  2 hémisphères.
tau_nh_sh_upper=1.e9 # va
tau_nh_sh_lower=1.e9
geff=1.
Catm=7. # = C in myclim, but rename to avoid conflict with C for ACtor
C0=100.
lam=1.
gamma=0.7
ndt=10




# ---------------- noise related parameters ------------------------------------
#1/ --- noise added to state variables at each time step
# noise_type type of noise. Possible values: "red","white" ou "mixed"
noise_type='red'
noise_T=0.15       #--in K
noise_monsoon=5.   #--in % change


# 2/ --- observation noises: the value of these noises is added to the state variables
#   before they are fed into the controller. They have not effect!
#   on the state variables.  
#TSRM_noise_obs_std : standard deviation of TSRM observation noise.
#                       mean value: 0
TSRM_noise_obs_std=0. # 1.e-2
#TSRMnh_noise_obs_std : standard deviation of TSRMnh observation noise.
#                       mean value: 0
TSRMnh_noise_obs_std=0. # 1.e-2
#TSRMsh_noise_obs_std : standard deviation of TSRMsh observation noise.
#                       mean value: 0
TSRMsh_noise_obs_std=0. # 1.e-2
# monsoon_noise_obs_std:  standard deviation of monsoon observation noise.
monsoon_noise_obs_std=0. # 1

# 3/ --- noise on emissions: noise added to emissions 
# eminoise[emipoint] = stdev noise on emission at emipoint
# this noise is taken as gaussian with mean=0
eminoisestd={"60N":1,
"30N":2,
"15N":2,
"eq":4,
"15S":3,
"30S":0,
"60S":0 }

#4/  noisefilei: file with noise input (temperatures and moonson)
#             takes precedence over all noise parameters.
noisefilei=""
# noisefileo: file to save noise.
noisefileo="noise-p.nc"


