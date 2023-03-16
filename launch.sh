#!/bin/bash

while true
do
    python3 src/main.py
    sleep $(($(date -d "20:00 tomorrow" +%s) - $(date +%s)))
done