#!/bin/bash

# Set your bot API key here
BOT_API_KEY="6089060960:AAEqhHfUVLgfnS0QsbEA4pcRl_jQ1STDQJM"
CHANNEL_ID="-1001907693181"
SCRIPT_PATH="src/test.py"

restart_script() {
    echo "Script terminated. Restarting in 1 minute..."
    sleep 60
    exec "$0"
}

# Function to exit the script gracefully
exit_script() {
    echo "Exiting script gracefully..."
    exit 0
}

# Trap to handle the script shutdown (SIGINT) and restart (SIGTERM)
trap exit_script SIGINT
trap restart_script SIGTERM

sendMessage(){
  # If the script exits, send a message to the channel indicating the bot crashed
curl -s -X POST "https://api.telegram.org/bot$BOT_API_KEY/sendMessage" \
  -d "chat_id=$CHANNEL_ID" \
  -d "text=The bot has crashed. Please check the logs and restart it."

}

# Infinite loop
while true; do
    # Your commands here
    python3 $SCRIPT_PATH
    sendMessage
done



