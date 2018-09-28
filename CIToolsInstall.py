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
	"""GitHub Installation handle"""
	MyOS.Clear()
	if ProgramMenu_Items["1"][2] == 'Installed':
		# GitHub Uninstaller

		if ProgramMenu.Confirm('Are you sure you want to remove {} from your machine.\nYou can always Reinstall it later.'.format(ProgramMenu_Items["1"][1])):
			os.system('sudo apt-get --purge remove -y git') # TODO switch from apt-get to Aptitude  Better functionality and easier to script I/O 
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
		if ProgramMenu.Confirm('Are you sure you want to remove {} from your machine.\nYou can always Reinstall it later.'.format(ProgramMenu_Items["2"][1])):
			os.system('sudo apt-get --purge remove -y build-essential') # TODO switch from apt-get to Aptitude  Better functionality and easier to script I/O 
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
	elif ProgramMenu.Confirm("Are you sure you want to remove {} from your machine.\nYou can always Reinstall it later.".format(ProgramMenu_Items["3"][1])):
        os.system('sudo apt-get --purge remove -y cifs-utils') # TODO switch from apt-get to Aptitude  Better functionality and easier to script I/O 
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
		if ProgramMenu.Confirm('Are you sure you want to remove {} from your machine.\nYou can always Reinstall it later.'.format(ProgramMenu_Items["4"][1])):
			os.system('sudo apt-get --purge remove -y openssh-server') # TODO switch from apt-get to Aptitude  Better functionality and easier to script I/O 
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
	ip_config() # TODO see what this is? missing intelisense
	print('Your IP is now Configured')
	time.sleep(DELAY)
	main()			

##############
##Functions ##
##############
# Debug function
def Debug(var1, var2, TF):
	DEBUG = True # TODO O_e >..< just omg DEBUG == True will RETURN TRUE DIRECTLY AFTER ASSIGNMENT O_e >..< bleh
	if DEBUG == True and TF == True: #
		print(var1 +' = ' + var2)	
			
# Print in color then reset color on end of line.
# TODO O_e can we please move this to the com class?
def colorPrint(txt,colorStart):
	print (colorStart+txt+'\033[0m')


# Main Entry Point
def main():
    """Main Entry point"""
    MyOS.Clear()
    print('Welcome',users,'to the Collective Industries Tools.') # TODO see where that users goes and why its not in the com class
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
            git() # TODO Make a task class to call values from a dict 
            break
        if case("2"):
            MyOS.Clear()
            print("Running GCC install/uninstall")
            time.sleep(DELAY)
            gcc() #
            break
        if case("3"):
            MyOS.Clear()
            print("Running CIFS Filesystem install/uninstall")
            time.sleep(DELAY)
            cifs() #
            break
        if case("4"):
            MyOS.Clear()
            print("Running SSH Server install/uninstall")
            time.sleep(DELAY)
            ssh() #
            break
        if case("8"):
            MyOS.Clear()
            print("Running IP Configuration")
            time.sleep(DELAY)
            IP() #
            break

# Pythons built in main entrypoint
# calls init and runs main loop
if __name__ == "__main__":
    # WTF? I cant even
    if user == '':
        users = uname
    else:
        users = user
	# Switch over to the main function
    main()	
