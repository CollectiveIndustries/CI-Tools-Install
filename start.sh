#!/bin/bash

# First off lets install the requirements.txt

sudo pip install -r requirements.txt

# TODO #4 move this block of code to an SH script. 
# Frankly if Python3 is _NOT INSTALLED_ how are we running this script?????
# def init(): 
#     """Check for and initilize dependancies"""
#     MyOS.ProgExists('python3')
#     MyOS.ProgExists('pip')
#     if MyOS.ProgExists('python3') == 'Not Installed':
#         os.system('sudo apt-get install -y python3')
    
#     global users
#     if user == '':
#         users = uname
#     else:
#         users = user
#     main_menu()