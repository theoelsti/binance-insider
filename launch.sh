#!/bin/bash
echo > errors.log

if ! command -v urlencode &> /dev/null
then
    echo "urlencode not found, attempting to install."
    if [ "$(uname)" == "Darwin" ]; then
        # Install on macOS
        brew install gridsite
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        # Install on Linux
        if [ -f /etc/debian_version ]; then
            # Debian/Ubuntu
            sudo apt-get update
            sudo apt-get install -y gridsite-clients
        elif [ -f /etc/redhat-release ]; then
            # CentOS/RHEL
            sudo yum install -y gridsite
        else
            echo "Unsupported Linux distribution. Please install gridsite manually."
            exit 1
        fi
    else
        echo "Unsupported operating system. Please install gridsite manually."
        exit 1
    fi
fi

# Set your bot API key here
BOT_API_KEY="[INSERT_YOUR_TELEGRAM_BOT_API_TOKEN]"
CHANNEL_ID="[INSERT_YOUR_TELEGRAM_CHANNEL]"
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
  req=$(curl -s -X POST "https://api.telegram.org/bot$BOT_API_KEY/sendMessage" \
    -d "chat_id=$CHANNEL_ID" \
    -d "parse_mode=markdown" \
    -d "text=$encoded_text")
}


# Infinite loop
while true; do
    # Run the Python script and redirect errors to the log file
    python3 $SCRIPT_PATH 2> errors.log
    
    # If the Python script exits with an error, send the log content
    if [ $? -ne 0 ]; then
        sendMessage
    fi
    if [ $? -eq 0 ]; then
        restart_script
    fi
done
