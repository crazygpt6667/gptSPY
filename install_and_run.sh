#!/bin/bash

echo "Installing SecureConnect Application..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed."
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

echo "Installing required packages..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install required packages."
    echo "Please check your internet connection and try again."
    exit 1
fi

echo
echo "Installation complete!"
echo
echo "Starting SecureConnect Application..."
python3 main.py