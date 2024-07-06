def set_experiment(exp):
  #--some keywords
  Kp='Kp' ; Ki='Ki' ; Kd='Kd' ; target='target' ; setpoint='setpoint' 
  emimin='emimin' ; emimax='emimax' ; emipoints='emipoints' ; stops='stops'
  t1='t1' ; t2='t2'
  #
  #--List of experiments with list of actors, type of setpoint, setpoint, emissions min/max and emission points
  #--single actor in NH emitting in his own hemisphere
  if exp=="1a":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'NHST',    setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15N'],t1:50,t2:70,stops:[]}
  #
  #--single actor in NH emitting in opposite hemisphere
  elif exp=="1b":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'NHST',    setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15S'],t1:50,t2:70,stops:[]}
  #
  #--single actor in SH emitting in opposite hemisphere
  elif exp=="1c":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'SHST',    setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15N'],t1:50,t2:70,stops:[]}
  #
  #--single actor in SH emitting in opposite hemisphere
  elif exp=="1d":
    A={Kp:0.008,Ki:0.006,Kd:0.0,target:'monsoon', setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15S'],t1:50,t2:70,stops:[]}
  #
  #--two actors with each one injection point in same hemisphere as their target
  elif exp=="2a":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'NHST',    setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15N'],t1:50,t2:70,stops:[]}
    B={Kp:0.8, Ki:0.6, Kd:0.0,target:'SHST',    setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15S'],t1:50,t2:70,stops:[]}
  #
  #--two actors with each one injection point in opposite hemisphere
  elif exp=="2b":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'NHST',    setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15S'],t1:50,t2:70,stops:[]}
    B={Kp:0.8, Ki:0.6, Kd:0.0,target:'SHST',    setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15N'],t1:50,t2:70,stops:[]}
  #
  #--two actors with each one injection point in same hemisphere but stops if overshoot (Anni's run)
  elif exp=="2c":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'NHST',    setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15N'],t1:50,t2:70,stops:[-0.1]}
    B={Kp:0.8, Ki:0.6, Kd:0.0,target:'SHST',    setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15S'],t1:50,t2:70,stops:[-0.1]}
  #
  #--two actors who each have two injection points and same limits
  elif exp=="3a":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'NHST',    setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15S','15N'],t1:50,t2:70,stops:[]}
    B={Kp:0.8, Ki:0.6, Kd:0.0,target:'SHST',    setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15S','15N'],t1:50,t2:70,stops:[]}
  #
  #--two actors who each have two injection points and different limits
  elif exp=="3b":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'NHST',    setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15S','15N'],t1:50,t2:70,stops:[]}
    B={Kp:0.8, Ki:0.6, Kd:0.0,target:'SHST',    setpoint:0.0, emimin:0.0,emimax:5.0,emipoints:['15S','15N'],t1:50,t2:70,stops:[]}
  #
  #--two actors with targets on NHST and monsoon
  elif exp=="4a":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'NHST',   setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15N'],t1:50,t2:70,stops:[]}
    B={Kp:0.08,Ki:0.06,Kd:0.0,target:'monsoon',setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15S'],t1:50,t2:70,stops:[]}
  #--two actors with targets on NHST and monsoon and stops for B in monsoon target overshoot
  elif exp=="4b":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'NHST',   setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15N'],t1:50,t2:70,stops:[]}
    B={Kp:0.08,Ki:0.06,Kd:0.0,target:'monsoon',setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['30S'],t1:50,t2:70,stops:[5.0]}
  #--two actors with targets on NHST and monsoon and B starts only on year 30 due to worsening of the monsoon
  elif exp=="4c":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'NHST',   setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15N'],t1:50,t2:70,stops:[]}
    B={Kp:0.08,Ki:0.06,Kd:0.0,target:'monsoon',setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15S'],t1:50,t2:70,stops:[(50,80)]}
  #--two actors with same targets on GMST
  elif exp=="5a":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'GMST',setpoint:0.0,emimin:0.0,emimax:10.0,emipoints:['eq'],t1:50,t2:70,stops:[]}
    B={Kp:0.9, Ki:0.5, Kd:0.0,target:'GMST',setpoint:0.0,emimin:0.0,emimax:10.0,emipoints:['eq'],t1:50,t2:70,stops:[]}
  #--two actors with same targets on GMST but one stop for A
  elif exp=="5b":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'GMST',setpoint:0.0,emimin:0.0,emimax:10.0,emipoints:['eq'],t1:50,t2:70,stops:[(100,120)]}
    B={Kp:0.9, Ki:0.5, Kd:0.0,target:'GMST',setpoint:0.0,emimin:0.0,emimax:10.0,emipoints:['eq'],t1:50,t2:70,stops:[]}
  #--two actors with same targets on GMST but multiple stops for A
  elif exp=="5c":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'GMST',setpoint:0.0,emimin:0.0,emimax:10.0,emipoints:['eq'],t1:50,t2:70,stops:[(100,110),(120,130),(140,150),(160,170)]}
    B={Kp:0.8, Ki:0.6, Kd:0.0,target:'GMST',setpoint:0.0,emimin:0.0,emimax:10.0,emipoints:['eq'],t1:50,t2:70,stops:[]}
  #--two actors with targets on GMST and stops for A if target overshoot
  elif exp=="5d":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'GMST',setpoint:0.0,emimin:0.0,emimax:10.0,emipoints:['eq'],t1:50,t2:70,stops:[-0.1]}
    B={Kp:0.8, Ki:0.6, Kd:0.0,target:'GMST',setpoint:0.0,emimin:0.0,emimax:10.0,emipoints:['eq'],t1:50,t2:70,stops:[]}
  #--two actors with targets on GMST and multiple stops for A and B
  elif exp=="5e":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'GMST',setpoint:0.0,emimin:0.0,emimax:10.0,emipoints:['eq'],t1:50,t2:70,stops:[(100,110),(120,130),(140,150),(160,170)]}
    B={Kp:0.8, Ki:0.6, Kd:0.0,target:'GMST',setpoint:0.0,emimin:0.0,emimax:10.0,emipoints:['eq'],t1:50,t2:70,stops:[(110,120),(130,140),(150,160),(170,180)]}
  #--two actors with targets on GMST and multiple (diff length) stops for A and B
  elif exp=="5f":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'GMST',setpoint:0.0,emimin:0.0,emimax:10.0,emipoints:['eq'],t1:50,t2:70,stops:[(100,115),(130,145),(160,175)]}
    B={Kp:0.8, Ki:0.6, Kd:0.0,target:'GMST',setpoint:0.0,emimin:0.0,emimax:10.0,emipoints:['eq'],t1:50,t2:70,stops:[(115,130),(145,160)]}  #
  #--three actors
  elif exp=="6":
    A={Kp:0.8, Ki:0.6, Kd:0.0,target:'NHST',   setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['15N'],t1:50,t2:70,stops:[]}
    B={Kp:0.08,Ki:0.06,Kd:0.0,target:'monsoon',setpoint:0.0, emimin:0.0,emimax:10.0,emipoints:['30S'],t1:50,t2:70,stops:[]}
    C={Kp:0.09,Ki:0.05,Kd:0.0,target:'monsoon',setpoint:10.0,emimin:0.0,emimax:10.0,emipoints:['15S'],t1:50,t2:70,stops:[]}
  else: 
    sys.exit('This scenario is not parametrized')
  #
  #--Initialise properties of Actors
  P={'A':A}
  if 'B' in vars(): P['B']=B
  if 'C' in vars(): P['C']=C
  if 'D' in vars(): P['D']=D
  #
  return P
