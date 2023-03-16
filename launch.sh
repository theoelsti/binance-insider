#!/bin/bash

while true
do
    python3 src/main.py
    sleep $(($(date -d "21:01" +%s) - $(date +%s)))
done