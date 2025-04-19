#!/usr/bin/env bash

if [ -z "$1" ]; then
  echo "Usage: $0 SELF_PORT [BOOTSTRAP_PORT]"
  exit 1
fi

SELF_PORT=$1
BOOTSTRAP_PORT=$2
# NOT GOING TO DECLARE GLOBAL ENVIRONMENT VARIABLES
# export SELF_PORT=$SELF_PORT
# if [ -n "$BOOTSTRAP_PORT" ]; then
#   export BOOTSTRAP_URL=http://localhost:$BOOTSTRAP_PORT
# fi

# Start backend  (Using inline environment variables such that they're not global)
if [ -n "$BOOTSTRAP_PORT" ]; then
  SELF_PORT=$SELF_PORT BOOTSTRAP_PORT=$BOOTSTRAP_PORT \
  uvicorn api:app --host 0.0.0.0 --port $SELF_PORT &
else
  SELF_PORT=$SELF_PORT \
  uvicorn api:app --host 0.0.0.0 --port $SELF_PORT &
fi
API_PID=$!

# Start UI (UI only needs SELF_PORT to communicate with API)
SELF_PORT=$SELF_PORT \
streamlit run ui.py --server.port $((SELF_PORT+500))

kill $API_PID
