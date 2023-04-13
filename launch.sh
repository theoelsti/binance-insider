#!/bin/bash

# Set your bot API key here
CONFIG_FILE="config/config.ini"
BOT_API_KEY=$(awk -F '=' '/bot_api_key/ {print $2}' $CONFIG_FILE | tr -d ' ')
CHANNEL_ID=$(awk -F '=' '/dev_channel_id/ {print $2}' $CONFIG_FILE | tr -d ' ')
SCRIPT_PATH="src/main.py"

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

sendMessage() {
  log_content=$(cat errors.log)
  # If the script exits, send a message to the channel indicating the bot crashed
  text="The bot has crashed. Please check the logs and restart it.\`\`\`$log_content\`\`\`"
  encoded_text=$(urlencode "$text")
  curl -s -X POST "https://api.telegram.org/bot$BOT_API_KEY/sendMessage" \
    -d "chat_id=$CHANNEL_ID" \
    -d "parse_mode=markdown" \
    -d "text=$encoded_text"
}


# Infinite loop
while true; do
    # Run the Python script and redirect errors to the log file
    python3 $SCRIPT_PATH --config $CONFIG_FILE 2> errors.log
    # If the Python script exits with an error, send the log content
    if [ $? -ne 0 ]; then
        sendMessage
    fi
    if [ $? -eq 0 ]; then
        restart_script
    fi
done
exit 0