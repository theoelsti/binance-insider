#!/bin/bash

while true
do
    python3 your_script.py
    sleep $(($(date -d "20:00 tomorrow" +%s) - $(date +%s)))
done