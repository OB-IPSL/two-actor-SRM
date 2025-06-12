#!/bin/bash
if [ x$1 == x ]; then
  i=5
else
  i=$1
fi
cas=1a-listek-gl-bruitnul-$i
python3 liste-kikp.py conf-${cas}.py
python3 traceliste.py -m1 -f out-${cas}.nc
