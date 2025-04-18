#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 PORT [BOOTSTRAP_PORT]"
  exit 1
fi

PORT=$1
BOOTSTRAP_PORT=$2
export PORT=$PORT
if [ -n "$BOOTSTRAP_PORT" ]; then
  export BOOTSTRAP_URL=http://localhost:$BOOTSTRAP_PORT
fi

# Start backend
uvicorn api:app --host 0.0.0.0 --port $PORT &
API_PID=$!

# Start UI
streamlit run ui.py --server.port $((PORT+500))

kill $API_PID
