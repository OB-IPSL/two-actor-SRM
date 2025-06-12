#!/bin/bash
for exp in 1a-listek-gl-bruitnul-3  1a-listek-gl-bruitnul-4    \
           1a-listek-gl-3  1a-listek-gl-4   ; do 
  ficconf=conf-${exp}.py
  ficnc=out-${exp}.nc
  python3 liste-kikp.py $ficconf
  python3 traceliste.py -f $ficnc
done
pdftk out-1a-listek-gl-*.pdf cat output out-1a-listek-gl.pdf

for i in 7 8 9 ; do
  ./liste.sh $i
done
