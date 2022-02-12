#!/bin/bash

# First off lets install the requirements.txt
if ! command -v python3 &> /dev/null
then
    sudo apt install python3 -y
else
    echo "Python3 already installed...."
fi

if ! command -v pip &> /dev/null
then
    sudo apt install pip -y
else
    echo "Pip already installed...."
fi

sudo pip install -r requirements.txt

# Set up configuration directory and touch the file.
# this file should be created using the installer file,
# however files already present shall be used.
mkdir -p config.d
touch config.d/main.cfg

# Now the environment is setup lets run the main install/configuration utility
python3 CIToolsInstall.py