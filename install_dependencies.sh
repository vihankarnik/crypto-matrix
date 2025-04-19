#!/usr/bin/env bash

# install all system-wide dependencies
pacman -S mingw-w64-x86_64-gcc \
          mingw-w64-x86_64-cmake \
          mingw-w64-x86_64-python \
          mingw-w64-x86_64-pybind11 \
          mingw-w64-x86_64-rust \
          mingw-w64-x86_64-pandas \
          mingw-w64-x86_64-python-pillow \
          mingw-w64-x86_64-python-pyarrow

# create a venv so that these python packages dont interfere with the global python installation
python3 -m venv venv --system-site-packages
source venv/bin/activate

python3 -m pip install -r requirements.txt
