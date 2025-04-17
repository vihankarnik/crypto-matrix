#!/usr/bin/env bash
set -e
python -m pip install -r requirements.txt

# build C++ → shared lib
cmake -B build && cmake --build build -j

# start API in background
python -m uvicorn main:app --reload --port 8000 &
API_PID=$!

# start UI (blocking)
streamlit run app.py

# cleanup
kill $API_PID
