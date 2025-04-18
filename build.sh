#!/usr/bin/env bash

# python3 -m venv venv
# source venv/bin/activate
# python -m pip install -r requirements.txt

# build C++ → shared lib
mkdir build
cd build
rm -rf ./*
cmake -G "MinGW Makefiles" .. && mingw32-make && cd ..
