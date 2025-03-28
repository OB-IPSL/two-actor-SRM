xs=np.zeros(4)
targets={"NHST":0.,
         "SHST":0.}
for tar in targets:
  xs[target2js[tar]]=targets[tar]
  poids[target2js[tar]]=1.
noise_T=0.
noise_monsoon=0.
tau=1.e9 #  test
emimaxl=20.
emipoint1='60N'
emipoint2='60S'
A={'Kp':0.8, 'Ki':0.6, 'Kd':0.0,'type':'NHST',    'setpoint':0.0, 'emimin':0.0,'emimax':emimaxl,'emipoints':[emipoint1],'t1':50,'t2':70,'stops':[]}
dicKp={'NHST': {emipoint1:0.8},
       'SHST': {emipoint2:0.8},
       'GMST': {},
       'monsoon' : {}}
dicKi={'NHST': {emipoint1:0.6},
       'SHST': {emipoint2:0.6},
       'GMST': {},
       'monsoon' : {}}
dicKd={'NHST': {},
       'SHST': {},
       'GMST': {},
       'monsoon' : {}}
aremipoints2 =[]
for dic in [dicKp,dicKi,dicKd]:
    for tt in dic:
      for emip in dic[tt]:
        if not emip in aremipoints2:
          aremipoints2.append(emip)
tau_nh_sh_upper=tau
tau_nh_sh_lower=tau
print("aremipoints2",aremipoints2)
