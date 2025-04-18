#!/usr/bin/env bash

if [ -z "$1" ]; then
  echo "Usage: $0 SELF_PORT [BOOTSTRAP_PORT]"
  exit 1
fi

SELF_PORT=$1
BOOTSTRAP_PORT=$2
export SELF_PORT=$SELF_PORT
if [ -n "$BOOTSTRAP_PORT" ]; then
  export BOOTSTRAP_URL=http://localhost:$BOOTSTRAP_PORT
fi

# Start backend
uvicorn api:app --host 0.0.0.0 --port $SELF_PORT &
API_PID=$!

# Start UI
streamlit run ui.py --server.port $((SELF_PORT+500))

kill $API_PID
