#!/usr/bin/python3
#coding:utf8

######################################
##									##
##		Collective Industries		##
##		 		Tools				##
##									##
##		  By: Levi & Andrew			##
##				©2018				##
######################################


#############
## Imports ##
#############
from sys import platform
import shutil
import distutils.spawn
import os
import subprocess
import getpass
import pwd
import getpass
import time

###############
## Variables ##
###############
global users
user = pwd.getpwuid(os.getuid())[4]
uname = getpass.getuser()
os_name	= os.name
user = user.replace(',', '')
_sleep_ = 2
#############
## Classes ##
#############
# Text output color definitions
class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
	
# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
# Located at http://code.activestate.com/recipes/410692/
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

#########################################
## Program Install/Uninstall Functions ##
#########################################
# GitHub Instal/Uninstall Function
def git():
	# GitHub Installation
	OSClear(oper)
	if str(prog_check('git')) == False:
		print('Getting ready to install GitHub.')
		time.sleep(_sleep_)
		os.system('wget https://raw.githubusercontent.com/hammerzaine/CI-Tools-Install/master/git_install.py')
		os.system('./git_install.py')
		print('GitHub is now installed')
		time.sleep(_sleep_)
		os.system('sudo rm -y git_install.py')
		main()
	else:
		# GitHub Uninstaller
		print('Are you sure you want to remove GitHub from your machine.')
		print ('You can always Reinstall it later.')
		yn = input('Y/N: ')
		if yn.lower() == 'y':
			print('Remove github here')
		else:
			main()
			
# CIFS Filesystem Install/Uninstall
def cifs():
	# CIFS Installation
	OSClear(oper)
	Debug('CIFS Program Check', str(prog_check('cifs-utils')), False)
	time.sleep(_sleep_)
	if prog_check('cifs-utils') == False:
		print('Getting ready to install CIFS Filesystem.')
		time.sleep(_sleep_)
		os.system('sudo wget https://raw.githubusercontent.com/hammerzaine/CI-Tools-Install/master/cifs_install.py')
		os.system('sudo chmod +x cifs_install.py')
		os.system('python cifs_install.py')
		print('CIFS Filesystem is now installed')
		time.sleep(_sleep_)
		os.system('sudo rm cifs_install.py')
		main()
	else:
		# CIFS Uninstaller
		print ('Are you sure you want to remove CIFS Filesytem from your machine.')
		print ('You can always Reinstall it later.')
		yn = input('Y/N: ')
		if yn.lower() == 'y':
			os.system('sudo apt-get remove -y cifs-utils')
			main()
		else:
			main()
##############
##Functions ##
##############
# Debug function
def Debug(var1, var2, TF):
	DEBUG = True
	if DEBUG == True and TF == True:
		print(var1 +' = ' + var2)	
			
# Print in color then reset color on end of line.
def colorPrint(txt,colorStart):
	print (colorStart+txt+'\033[0m')
	
# Determines what O/S you are running
def GetOS():
	_SystemOS_ = platform.strip()
	Debug("startup(): _SystemOS_",_SystemOS_,False)
	if (_SystemOS_ == 'linux' or _SystemOS_ == 'linux2'):
		# linux
		with open('/etc/os-release') as file:
			oper = file.readlines()
			oper = oper[5].split('=')
			return oper[1].strip() # Grab OS release Name we want to know what flavor of lenny we use.
	elif(_SystemOS_ == 'win32'):
		return _SystemOS_

# Determins out to clear your screen 
def OSClear(osname):
	if(osname == "win32"):
		os.system("cls")
	else: # well its not Windows we can just "clear"
		os.system("clear")
              
# Checks to see if a program is installed or not
def prog_check(program): 
	return shutil.which(program) is not None

# Initial function	
def init():
	# Checks to see what O/S yor running and set the variable
	global oper
	oper = GetOS()
	# Checks to see if to use username or real name
	global users
	if user == '':
		users = uname
	else:
		users = user
	# Switch over to the main function
	main()	
	# Checks to see if python 3 is installed. If not, install it
	
# Main function
def main():
	OSClear(oper)
	##########
	## Menu ##
	##########
	print ('Welcome',users,'to the Collective Industries Tools.')
	print ('')
	print ('Installations')
	print ('1. GitHUB          -',str(prog_check('git')))
	print ('2. GCC             -',str(prog_check('gcc')))
	print ('3. CIFS Filesystem -',str(prog_check('cifs-utils')))
	print ('1. SSH Server      -',str(prog_check('openssh')))
	print ('')
	print ('Configurations')
	print ('4. Set IP to Static/Dynamic')
	print ('5. Config 2')
	print ('')
	print ('0. Exit')
	print ('')
	
	for case in switch(input('Select: ')):
		if case("0"):
			exit()
			break
		if case("1"):
			OSClear(oper)
			print("Running GitHub install/uninstall")
			time.sleep(_sleep_)
			git()
			break
		if case("2"):
			pass
			break
		if case("3"):
			OSClear(oper)
			print("Running CIFS Filesystem install/uninstall")
			time.sleep(_sleep_)
			cifs()
			break
	
##################
## Main Program ##
##################
# Start the main function and start the program
init()
