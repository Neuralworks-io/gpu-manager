#!/bin/bash
echo "> now ing app pid find!"
CURRENT_PID=$(pgrep -f start-gpu-manager.py)
echo "$CURRENT_PID"
if [ -z $CURRENT_PID ]; then
        echo "> no ing app."
else
        echo "> kill -9 $CURRENT_PID"
        kill -9 $CURRENT_PID
        sleep 3
fi
echo "> new app deploy"
PY_NAME=$(ls |grep 'gpu-manager' | tail -n 1)
echo "> PY Name: $PY_NAME"

nohup python3 $PY_NAME &
sleep 3
