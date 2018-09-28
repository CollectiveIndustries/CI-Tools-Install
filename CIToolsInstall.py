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
from lib import com
import shutil, os, subprocess, getpass, time, menu, progs

# Build an OS Object
MyOS = com._OS_()

user = ""
## Unix Only Imports
if MyOS._type_ != "win32":
    import pwd # no module found, UNIX systems ONLY
    import apt
    user = pwd.getpwuid(os.getuid())[4]

###############
## Variables ##
###############
global users
uname = getpass.getuser()
os_name	= os.name
user = user.replace(',', '')
DELAY = 2

##################
## Menu Builder ##
##################
ProgramMenu_Header = ["#","Program","Installed"]
ProgramMenu_Items  = {"1":["GitHub", MyOS.ProgExists('git')],
                      "2":["GCC",MyOS.ProgExists('build-essential')],
                      "3":["CIFS Filesystem",MyOS.ProgExists('cifs-utils')],
                      "4":["SSH Server",MyOS.ProgExists('openssh-server')],
                      "5":["MySQL Server",MyOS.ProgExists('mysql-server')],
                      "6":["MariaDB Server",MyOS.ProgExists('mariadb-server')],
                      "7":["Apache",MyOS.ProgExists('apache2')],
                      "8":["Dos 2 Unix converter",MyOS.ProgExists('dos2unix')]}

OptionsMenu_Header = ["#", "Settings"]
OptionsMenu_Items  = {"9":["IP Config"],
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
	"""GitHub Installation"""
	MyOS.Clear()
	if ProgramMenu_Items["1"][2] == 'Installed':
		# GitHub Uninstaller

        # TODO Confrim uninstall
		print('Are you sure you want to remove GitHub from your machine.')
		print ('You can always Reinstall it later.')
		yn = input('Y/N: ')
		if yn.lower() == 'y':
			os.system('sudo apt-get --purge remove -y git')
		else:
			main()
	else:
		print('Getting ready to install GitHub.')
		time.sleep(DELAY)
		git_install()
		print('GitHub is now installed')
		time.sleep(DELAY)
		main()
	

def gcc():
	"""GitHub Instal/Uninstall Function"""
	MyOS.Clear()
	if ProgramMenu_Items["2"][2] == 'Installed': 
		# GCC Uninstaller

        # TODO Wait another confirm box?
		print('Are you sure you want to remove GCC from your machine.')
		print ('You can always Reinstall it later.')
		yn = input('Y/N: ')
		if yn.lower() == 'y':
			os.system('sudo apt-get --purge remove -y build-essential')
		else:
			main()
	else:
		print('Getting ready to install GCC.')
		time.sleep(DELAY)
		gcc_install()
		print('GCC is now installed')
		time.sleep(DELAY)
		main()
				
# CIFS Filesystem Install/Uninstall
def cifs():
	# CIFS Installation
	MyOS.Clear()
	Debug('CIFS Program Check', ProgramMenu_Items["3"][2], False) 
	time.sleep(DELAY)
	if ProgramMenu_Items["3"][2] == False:
		print('Getting ready to install CIFS Filesystem.')
		time.sleep(DELAY)
		cifs_install()
		print('CIFS Filesystem is now installed')
		time.sleep(DELAY)
		main()
	else:
		# CIFS Uninstaller

        # TODO Holy cow guess what? yup another confirm
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
	Debug('SSH Program Check', ProgramMenu_Items["4"][2], False) 
	time.sleep(DELAY)
	if ProgramMenu_Items["4"][2] == False: 
		print('Getting ready to install SSH Server.')
		time.sleep(DELAY)
		ssh_install()
		print('SSH Server is now installed')
		time.sleep(DELAY)
		main()
	else:
		# SSH Uninstaller

        # TODO YES!! im sure Remove the damn thing
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
	time.sleep(DELAY)
	ip_config()
	print('Your IP is now Configured')
	time.sleep(DELAY)
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
    """Main Entry point"""
    MyOS.Clear()
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
            time.sleep(DELAY)
            git()
            break
        if case("2"):
            MyOS.Clear()
            print("Running GCC install/uninstall")
            time.sleep(DELAY)
            gcc()
            break
        if case("3"):
            MyOS.Clear()
            print("Running CIFS Filesystem install/uninstall")
            time.sleep(DELAY)
            cifs()
            break
        if case("4"):
            MyOS.Clear()
            print("Running SSH Server install/uninstall")
            time.sleep(DELAY)
            ssh()
            break
        if case("8"):
            MyOS.Clear()
            print("Running IP Configuration")
            time.sleep(DELAY)
            IP()
            break

##################
## Main Program ##
##################
# Start the main function and start the program
init()
