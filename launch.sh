#!/bin/bash

while true
do
    python3 src/main.py
    print
    sleep $(($(date -d "20:00" +%s) - $(date +%s)))
done