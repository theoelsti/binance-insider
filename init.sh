#!/bin/bash
echo > errors.log

# Check for Python3 and PIP installation
if ! command -v python3 &> /dev/null
then
    echo "Python3 not found, attempting to install."
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        sudo apt-get update
        sudo apt-get install -y python3
    elif [ -f /etc/redhat-release ]; then
        # CentOS/RHEL
        sudo yum install -y python3
    else
        echo "Unsupported Linux distribution. Please install Python3 manually."
        exit 1
    fi
fi

if ! command -v pip &> /dev/null
then
    echo "pip not found, attempting to install."
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        sudo apt-get update
        sudo apt-get install -y python3-pip
    elif [ -f /etc/redhat-release ]; then
        # CentOS/RHEL
        sudo yum install -y python3-pip
    else
        echo "Unsupported Linux distribution. Please install pip manually."
        exit 1
    fi
fi

# Check for urlencode installation
if ! command -v urlencode &> /dev/null
then
    echo "urlencode not found, attempting to install."
    if [ "$(uname)" == "Darwin" ]; then
        # Install on macOS
        brew install gridsite
    elif [ "$(expr substr "$(uname -s)" 1 5)" == "Linux" ]; then
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

# Check for MySQL installation
if ! command -v mysql &> /dev/null
then
    echo "MySQL not found, attempting to install."
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        sudo apt-get update
        sudo apt-get install -y mysql-server
    elif [ -f /etc/redhat-release ]; then
        # CentOS/RHEL
        sudo yum install -y mysql-server
    else
        echo "Unsupported Linux distribution. Please install MySQL manually."
        exit 1
    fi
fi
pip3 install -r requirements.txt
exit 0
