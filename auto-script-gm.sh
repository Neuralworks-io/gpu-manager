#!/bin/bash
echo "> now ing app pid find!"
CURRENT_PIDS=$(pgrep -f start-gpu-manager.py)
if [ -z "$CURRENT_PIDS" ]; then
  echo "> no ing app."
else
  echo "$CURRENT_PIDS"
  for PID in $CURRENT_PIDS; do
    echo "> kill -9 $PID"
    kill -9 "$PID"
    sleep 3
  done
fi
echo "> new app deploy"
nohup python3 start-gpu-manager.py &
sleep 3
