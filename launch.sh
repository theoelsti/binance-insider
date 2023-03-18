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
trap restart_script SIGINT SIGTERM
# Start the Python script
python3 $SCRIPT_PATH
restart_script() {
    echo "Script terminated. Restarting in 1 minute..."
    sleep 60
    exec "$0"
}
exit_script() {
    echo "Exiting script gracefully..."
    exit 0
}

sendMessage(){
  # If the script exits, send a message to the channel indicating the bot crashed
curl -s -X POST "https://api.telegram.org/bot$BOT_API_KEY/sendMessage" \
  -d "chat_id=$CHANNEL_ID" \
  -d "text=The bot has crashed. Please check the logs and restart it."

}

# Trap to handle the script shutdown (SIGINT) and restart (SIGTERM)
trap exit_script SIGINT
trap restart_script SIGTERM

# Infinite loop
while true; do
    # Your commands here
    python3 $SCRIPT_PATH
    sendMessage
done



