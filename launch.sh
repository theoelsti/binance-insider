#!/bin/bash

# Set your bot API key here
BOT_API_KEY="6089060960:AAEqhHfUVLgfnS0QsbEA4pcRl_jQ1STDQJM"
CHANNEL_ID="-1001907693181"
SCRIPT_PATH="src/main.py"

# Start the Python script
python3 $SCRIPT_PATH

# If the script exits, send a message to the channel indicating the bot crashed
curl -s -X POST "https://api.telegram.org/bot$BOT_API_KEY/sendMessage" \
  -d "chat_id=$CHANNEL_ID" \
  -d "text=The bot has crashed. Please check the logs and restart it."

