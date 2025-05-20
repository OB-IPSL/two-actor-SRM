#!/bin/bash

echo "nh"
python3 carte-kikp.py conf-1a-kikp-nh.py
echo "gl"
python3 carte-kikp.py conf-1a-kikp-gl.py
echo "sh"
python3 carte-kikp.py conf-1a-kikp-sh.py
echo "nh bruit nul"
python3 carte-kikp.py conf-1a-kikp-gl-bruitnul.py
echo "gl bruit nul"
python3 carte-kikp.py conf-1a-kikp-nh-bruitnul.py
echo "sh bruit nul"
python3 carte-kikp.py conf-1a-kikp-sh-bruitnul.py
