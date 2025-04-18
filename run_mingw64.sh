#!/usr/bin/env bash
# set -e

# build C++ → shared lib
mkdir build
cd build
rm -rf ./*
cmake -G "MinGW Makefiles" .. && mingw32-make && cd ..

# start API in background
# python -m uvicorn main:app --reload --port 8000 &
# API_PID=$!

# start UI (blocking)
# streamlit run app.py

# cleanup
# kill $API_PID

