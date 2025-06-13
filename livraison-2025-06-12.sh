#!/bin/bash
python3 tracecarte.py --ki --kp -f out-1a-kikp-gl-3
mv out-1a-kikp-gl-3-normes.pdf out-1a-kikp-gl-3-normes-1.pdf
python3 tracecarte.py --n2max=0.02 --n1max=0.2 --ki --kp -f out-1a-kikp-gl-3
mv out-1a-kikp-gl-3-normes.pdf out-1a-kikp-gl-3-normes-2.pdf


