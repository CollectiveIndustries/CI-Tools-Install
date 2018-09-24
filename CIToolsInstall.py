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
import shutil
import os
import subprocess
import getpass
import time
import menu
from lib import com

# Build an OS Object
MyOS = com._OS_()

## Unix Only Imports
if MyOS._type_ != "win32":
    import pwd # no module found, UNIX systems ONLY
    import apt

###############
## Variables ##
###############
global users

if MyOS._type_ != "win32":
    user = pwd.getpwuid(os.getuid())[4]
else:
    user = ""

uname = getpass.getuser()
os_name	= os.name
user = user.replace(',', '')
_sleep_ = 2

##################
## Menu Builder ##
##################
ProgramMenu_Header = ["Option","Program","Installed"]
ProgramMenu_Items  = {"1":["GitHub", MyOS.ProgExists('git')],
                      "2":["GCC",MyOS.ProgExists('build-essential')],
                      "3":["CIFS Filesystem",MyOS.ProgExists('cifs-utils')],
                      "4":["SSH Server",MyOS.ProgExists('openssh-server')],
                      "5":["MySQL Server",MyOS.ProgExists('mysql-server')],
                      "6":["MariaDB Server",MyOS.ProgExists('mariadb-server')],
                      "7":["Apache",MyOS.ProgExists('apache2')]}

OptionsMenu_Header = ["", "Settings"]
OptionsMenu_Items  = {"8":["IP Config"],
                      "E":["Exit"]
                     }

ProgramMenu = menu.TextMenu(ProgramMenu_Items,ProgramMenu_Header)
ProgramMenu.Align(ProgramMenu_Header[0],"c")
ProgramMenu.Align(ProgramMenu_Header[1],"l")
ProgramMenu.Align(ProgramMenu_Header[2],"r")

OptionsMenu = menu.TextMenu(OptionsMenu_Items,OptionsMenu_Header)
OptionsMenu.Align(OptionsMenu_Header[1],"l")

#########################################
## Program Install/Uninstall Functions ##
#########################################
# GitHub Instal/Uninstall Function
def git():
	# GitHub Installation
	MyOS.Clear()
	if str(MyOS.ProgExists('git')) == 'Installed':
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
	MyOS.Clear()
	if MyOS.ProgExists('build-essential') == 'Installed':
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
	MyOS.Clear()
	Debug('CIFS Program Check', str(MyOS.ProgExists('cifs-utils')), False)
	time.sleep(_sleep_)
	if MyOS.ProgExists('cifs-utils') == False:
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
	MyOS.Clear()
	Debug('SSH Program Check', str(MyOS.ProgExists('openssh-server')), False)
	time.sleep(_sleep_)
	if MyOS.ProgExists('openssh-server') == False:
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
	MyOS.Clear()
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
	


	#chk = os.system('aptitude show ' + program)
	#chk = file.readlines()
	#chk = chk[1].split(':')
	#return chk[1].strip()

	#if :
	#	return colorPrint('Installed',color.OKGREEN)
	#else:
	#	return colorPrint('Not Installed',color.FAIL)


# Initial function	
def init():
	# Checks to see what O/S yor running and set the variable
	# Checks to see if to use username or real name
	global users
	if user == '':
		users = uname
	else:
		users = user
	# Switch over to the main function
	main()	
	# Checks to see if python 3 is installed. If not, install it
	


# Main Entry Point
def main():
    MyOS.Clear()
    ###############
    ## Main Menu ##
    ###############
    print('Welcome',users,'to the Collective Industries Tools.')
    print('')
    print('Installations')
    ProgramMenu.Print()
    OptionsMenu.Print()
    print("")

    for case in com.switch(input('Select: ').lower()):
        if case("e"):
            exit()
            break
        if case("1"):
            MyOS.Clear()
            print("Running GitHub install/uninstall")
            time.sleep(_sleep_)
            git()
            break
        if case("2"):
            MyOS.Clear()
            print("Running GCC install/uninstall")
            time.sleep(_sleep_)
            gcc()
            break
        if case("3"):
            MyOS.Clear()
            print("Running CIFS Filesystem install/uninstall")
            time.sleep(_sleep_)
            cifs()
            break
        if case("4"):
            MyOS.Clear()
            print("Running SSH Server install/uninstall")
            time.sleep(_sleep_)
            ssh()
            break
        if case("8"):
            MyOS.Clear()
            print("Running IP Configuration")
            time.sleep(_sleep_)
            IP()
            break

##################
## Main Program ##
##################
# Start the main function and start the program
init()
