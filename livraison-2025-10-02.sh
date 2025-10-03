#!/bin/bash
for exp in 1a 11a 4c  ;  do
  python3 effet-cki-ckp.py --noise bruit1.txt -m --factor 2  --exp=$exp -o exp-${exp}-facteur-2.pdf
done
#python3 compare-exp.py --noise bruit1.txt 1a 11a -o comp-1a-11a.pdf
#python3 compare-exp.py --noise bruit1.txt 4c 24c -o comp-4c-24c.pdf
