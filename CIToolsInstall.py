#!/usr/bin/python3

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
import platform

from pytest import ExitCode
from lib import com
from shutil import which
from progs import Program
import os, pwd, time, subprocess, sys
import users

###############
## Variables ##
###############
DELAY = 2
global usr

# Build Objecs
MyOS = com._OS_()
usr = users.MyUser()

## Unix Only Imports
if MyOS._type_ != "win32":
    import pwd # no module found, UNIX systems ONLY
    import apt
    user = pwd.getpwuid(os.getuid())[4]

######################################################################

##############
##Functions ##
##############

# Debug function
def Debug(var1, var2, TF):
	DEBUG = True # flip de switch >..<
	if DEBUG == True and TF == True: #
		print(var1 +' = ' + var2)

######################################################################

###############
## Main Menu ##
###############

def BuildMenu():
    print('')
    print('Installations') # TODO #3 Compact into Key=Value pair for easy list creation for custom prog lists
    print('1. GitHub ............... ', MyOS.ProgExists('git'))
    print('2. GCC .................. ', MyOS.ProgExists('build-essential'))
    print('3. CIFS Filesystem ...... ', MyOS.ProgExists('cifs-utils'))
    print('4. SSH Server ........... ', MyOS.ProgExists('openssh-server'))
    print('5. MySQL Server ......... ', MyOS.ProgExists('mysql-server'))
    print('6. MariaDB Server ....... ', MyOS.ProgExists('mariadb-server'))
    print('7. Apache ............... ', MyOS.ProgExists('apache2'))
    print('8. Dos 2 Unix Converter . ', MyOS.ProgExists('dos2unix'))
    print('9. Midnight Commander ... ', MyOS.ProgExists('mc'))
    print('10. Log Navigator ....... ', MyOS.ProgExists('lnav'))
    print('')
    print('Configurations')
    #print('8. Set IP to Static/Dynamic')
    #print('9. Config 2')
    print('')
    print('E. Exit')
    print('')

####################################################################################


####################
## Configurations ##
####################
# TODO #6 Network Module
def IP():
	MyOS.Clear()
	print('Getting ready to Reconfigure your IP')
	time.sleep(DELAY)
	# ip_config() # TODO see what this is? missing intelisense
	print('Your IP is now Configured')
	time.sleep(DELAY)
	main()


####################################################################################

def main():
    """Main Entry point"""
    MyOS.Clear()
    usr.Login() # Handle login prompt externally

    ####################
    ## Program Driver ##
    ####################

    while True:
        MyOS.Clear()  
        BuildMenu()
        option = input('Select: ').lower()
        if option.lower() == 'e':
            exit(0)
                
# Pythons built in main entrypoint
# calls init and runs main loop
if __name__ == "__main__":
	# Switch over to the main function
    main()