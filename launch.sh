#!/bin/bash

while true
do
    python3 src/main.py
    echo "Script killed"
    sleep $(($(date -d "21:05" +%s) - $(date +%s)))
done