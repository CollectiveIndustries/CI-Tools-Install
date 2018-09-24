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
import os
import subprocess
import getpass
import pwd
import getpass
import time
import apt #For file checking

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
	if str(prog_check('git')) == 'Installed':
		# GitHub Uninstaller
		print('Are you sure you want to remove GitHub from your machine.')
		print ('You can always Reinstall it later.')
		yn = input('Y/N: ')
		if yn.lower() == 'y':
			os.system('sudo apt-get --purge remove -y git')
		else:
			main()
	else:
		print('Getting ready to install GitHub.')
		time.sleep(_sleep_)
		os.system('wget https://raw.githubusercontent.com/hammerzaine/CI-Tools-Install/master/git_install.py')
		os.system('sudo chmod +x git_install.py')
		os.system('python git_install.py')
		print('GitHub is now installed')
		time.sleep(_sleep_)
		os.system('sudo rm -y git_install.py')
		main()
	
# GitHub Instal/Uninstall Function
def gcc():
	# GCC Installation
	OSClear(oper)
	if prog_check('build-essential') == 'Installed':
		# GCC Uninstaller
		print('Are you sure you want to remove GCC from your machine.')
		print ('You can always Reinstall it later.')
		yn = input('Y/N: ')
		if yn.lower() == 'y':
			os.system('sudo apt-get --purge remove -y build-essential')
		else:
			main()
	else:
		print('Getting ready to install GCC.')
		time.sleep(_sleep_)
		os.system('wget https://raw.githubusercontent.com/hammerzaine/CI-Tools-Install/master/gcc_install.py')
		os.system('sudo chmod +x gcc_install.py')
		os.system('python gcc_install.py')
		print('GCC is now installed')
		time.sleep(_sleep_)
		os.system('sudo rm -y gcc_install.py')
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
			os.system('sudo apt-get --purge remove -y cifs-utils')
			main()
		else:
			main()

# SSH Server Install/Uninstall
def ssh():
	# SSH Installation
	OSClear(oper)
	Debug('SSH Program Check', str(prog_check('openssh-server')), False)
	time.sleep(_sleep_)
	if prog_check('openssh-server') == False:
		print('Getting ready to install SSH Server.')
		time.sleep(_sleep_)
		os.system('sudo wget https://raw.githubusercontent.com/hammerzaine/CI-Tools-Install/master/ssh_install.py')
		os.system('sudo chmod +x ssh_install.py')
		os.system('python ssh_install.py')
		print('SSH Server is now installed')
		time.sleep(_sleep_)
		os.system('sudo rm ssh_install.py')
		main()
	else:
		# SSH Uninstaller
		print ('Are you sure you want to remove SSH Server from your machine.')
		print ('You can always Reinstall it later.')
		yn = input('Y/N: ')
		if yn.lower() == 'y':
			os.system('sudo apt-get --purge remove -y openssh-server')
			main()
		else:
			main()

####################
## Configurations ##
####################
# IP Configuration
def IP():
	OSClear(oper)
	print('Getting ready to Reconfigure your IP')
	time.sleep(_sleep_)
	os.system('wget https://raw.githubusercontent.com/hammerzaine/CI-Tools-Install/master/ip_config.py')
	os.system('sudo chmod +x ip_config.py')
	os.system('python ip_config.py')
	print('Your IP is now Configured')
	time.sleep(_sleep_)
	os.system('sudo rm ip_config.py')
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
	#chk = os.system('aptitude show ' + program)
	#chk = file.readlines()
	#chk = chk[1].split(':')
	#return chk[1].strip()
	
	#if :
	#	return colorPrint('Installed',color.OKGREEN)
	#else:
	#	return colorPrint('Not Installed',color.FAIL)
		
def chk_install():
	global _git_
	global _gcc_
	global _cifs_
	global _sshs_
	global _sql_
	global _mdb_
	global _apa_
	_git_ = str(prog_check('git'))
	_gcc_ = str(prog_check('build-essential'))
	_cifs_ = str(prog_check('cifs-utils'))
	_sshs_ = str(prog_check('openssh-server'))
	_sql_ = str(prog_check('mysql-server'))
	_mdb_ = str(prog_check('mariadb-server'))
	_apa_ = str(prog_check('apache2'))
	
# Initial function	
def init():
	# Checks to see what O/S yor running and set the variable
	global oper
	oper = GetOS()
	chk_install()
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
	###############
	## Main Menu ##
	###############
	print ('Welcome',users,'to the Collective Industries Tools.')
	print ('')
	print ('Installations')
	print ('1. GitHub          - ' + _git_)
	print ('2. GCC             - ' + _gcc_)
	print ('3. CIFS Filesystem - ' + _cifs_)
	print ('4. SSH Server      - ' + _sshs_)
	print ('5. MySQL Server    - ' + _sql_)
	print ('6. MariaDB Server  - ' + _mdb_)
	print ('7. Apache          - ' + _apa_)
	print ('')
	print ('Configurations')
	print ('8. Set IP to Static/Dynamic')
	print ('9. Config 2')
	print ('')
	print ('E. Exit')
	print ('')
	
	for case in switch(input('Select: ').lower()):
		if case("e"):
			exit()
			break
		if case("1"):
			OSClear(oper)
			print("Running GitHub install/uninstall")
			time.sleep(_sleep_)
			git()
			break
		if case("2"):
			OSClear(oper)
			print("Running GCC install/uninstall")
			time.sleep(_sleep_)
			gcc()
			break
		if case("3"):
			OSClear(oper)
			print("Running CIFS Filesystem install/uninstall")
			time.sleep(_sleep_)
			cifs()
			break
		if case("4"):
			OSClear(oper)
			print("Running SSH Server install/uninstall")
			time.sleep(_sleep_)
			ssh()
			break
		if case("8"):
			OSClear(oper)
			print("Running IP Configuration")
			time.sleep(_sleep_)
			IP()
			break
	
##################
## Main Program ##
##################
# Start the main function and start the program
init()
