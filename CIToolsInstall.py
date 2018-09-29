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
from progs import Program
import users
import shutil, os, subprocess, getpass, time, menu, progs

# Build Objecs
MyOS = com._OS_()
global usr
usr = users.MyUser()

## Unix Only Imports
if MyOS._type_ != "win32":
    import pwd # no module found, UNIX systems ONLY
    import apt
    user = pwd.getpwuid(os.getuid())[4]

###############
## Variables ##
###############
os_name	= os.name
DELAY = 2

##################
## Menu Builder ##
##################
ProgramMenu_Header = ["#","Program","Installed"]

# Menu options on back end
ProgramLST = [Program('git'),
              Program('build-essential'),
              Program('cifs-utils'),
              Program('openssh-server'),
              Program('mysql-server'),
              Program('mariadb-server'),
              Program('apache2'),
              Program('dos2unix')]

ProgramMenu_Items  = {1:["GitHub",ProgramLST[0].installedStr],
                      2:["GCC",ProgramLST[1].installedStr],
                      3:["CIFS Filesystem",ProgramLST[2].installedStr],
                      4:["SSH Server",ProgramLST[3].installedStr],
                      5:["MySQL Server",ProgramLST[4].installedStr],
                      6:["MariaDB Server",ProgramLST[5].installedStr],
                      7:["Apache",ProgramLST[6].installedStr],
                      8:["Dos 2 Unix converter",ProgramLST[7].installedStr]}

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

####################
## Program Driver ##
####################

def CallProg(proglist=[],usrChoice=1):
    """Compares the prog list with the menu dict and calls the setup()"""
    indx = usrChoice-1
    print("Prog: {}\nIndex: {}\n###\n".format(proglist[indx].ProgName,indx))
    proglist[indx].UserEntryPoint()

#########################################
## Program Install/Uninstall Functions ##
#########################################
# GitHub Install/Uninstall Function
def git():
    """GitHub Installation handle"""
    MyOS.Clear()
    install_check('git', '1')
    #if ProgramMenu_Items["1"][2] == 'Installed':
    # GitHub Uninstaller

    #    if ProgramMenu.Confirm('Are you sure you want to remove {} from your machine.\nYou can always Reinstall it later.'.format(ProgramMenu_Items["1"][1])):
    #        os.system('sudo apt-get --purge remove -y git') # TODO switch from apt-get to Aptitude  Better functionality and easier to script I/O 
    #    else:
    #        main()
    #else:
    #    print('Getting ready to install GitHub.')
    #    time.sleep(DELAY)
    #    git_install()
    #    print('GitHub is now installed')
    #    time.sleep(DELAY)
    #    main()

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
	DEBUG = True # flip de switch >..<
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
    # grab user once
    usr.Login() # Handle login prompt externally
    MyOS.Clear()

    print('Welcome to the Collective Industries Tools.')
    print('')
    print('Installations')
    ProgramMenu.Print()
    OptionsMenu.Print()
    print("")

    option = input('Select: ').lower()

    # if its a program option run an full upgrade and then run program
    if int(option) <= len(ProgramLST): 
        progs.Upgrade(usr.PassWord)
        CallProg(ProgramLST,int(option))

    for case in com.switch(option): # define only non program menu options I.E Letters
        if case("e"):
            exit(0)
            break


# Pythons built in main entrypoint
# calls init and runs main loop
if __name__ == "__main__":
	# Switch over to the main function
    main()