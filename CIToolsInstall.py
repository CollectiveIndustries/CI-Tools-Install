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
from shutil import which
from progs import Program
import os, pwd, time, subprocess

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
DELAY = 2
oper = ''
os_name = os.name
install_check = ''
user = pwd.getpwuid(os.getuid()) [4]
option = ''

###############
## Functions ##
###############
def GetOS():
    """Determins what O/S you are running"""
    _SystemOS_ == platform.strip()
    if (_SystemOS_ == 'linux' or _SystemOS_ == 'linux2'):
        """Linux"""
        with open('/etc/os-release') as file:
            oper = file.readlines()
            oper = oper[5].split('=')
            return oper[1].strip() # Grab OS release Name we want to know what flavor of linux we use.
        elif(_SystemOS_ == 'win32'):
            return _SystemOS_

def OSClear(osname):
    """Determins how to clear your screen"""
    if(osname == "win32"):
        os.system("cls")
    else: # well its not Windows we can just "clear"
        os.system("clear")

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    program = which(name)
    if program == None:
        install_check = "Not Installed"
    else:
        install_check = "Installed" 
    return install_check

def init():
    oper = GetOS()
    is_tool('python3')
    is_tool('pip')
    if is_tool('python3') == 'Not Installed':
        os.system('sudo apt-get install -y python3')
    
    global users
    if user == '':
        users = uname
    else:
        users = user
    main_menu()

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
              Program('dos2unix'),
              Program('mc')]

ProgramMenu_Items  = {1:["GitHub",ProgramLST[0].installedStr],
                      2:["GCC",ProgramLST[1].installedStr],
                      3:["CIFS Filesystem",ProgramLST[2].installedStr],
                      4:["SSH Server",ProgramLST[3].installedStr],
                      5:["MySQL Server",ProgramLST[4].installedStr],
                      6:["MariaDB Server",ProgramLST[5].installedStr],
                      7:["Apache",ProgramLST[6].installedStr],
                      8:["Dos 2 Unix converter",ProgramLST[7].installedStr],
                      9:["Mindnight Commander",ProgramLST[8].installedStr]}

OptionsMenu_Header = ["#", "Settings"]
OptionsMenu_Items  = {"10":["IP Config"],
                      "E":["Exit"]
                     }

ProgramMenu = menu.TextMenu(ProgramMenu_Items,ProgramMenu_Header)
ProgramMenu.Align(ProgramMenu_Header[0],"c")
ProgramMenu.Align(ProgramMenu_Header[1],"l")
ProgramMenu.Align(ProgramMenu_Header[2],"r")

OptionsMenu = menu.TextMenu(OptionsMenu_Items,OptionsMenu_Header)
OptionsMenu.Align(OptionsMenu_Header[1],"l")

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

def TitleHeader():
    """Get creative and make it look COOL!!!!"""
    print('Welcome to the Collective Industries Tools.')
    print('')
    print('Installations')

# Main Entry Point
def main():
    """Main Entry point"""
    MyOS.Clear()
    # grab user once
    usr.Login() # Handle login prompt externally
    while True:
        MyOS.Clear() # Clear screen every time we redraw menu
        ProgramMenu.Print()
        OptionsMenu.Print()
        print("")

        option = input('Select: ').lower()
        
        ####################
        ## Program Driver ##
        ####################
        # if its a program option then run program object entrypoint
        try:
            if int(option) <= len(ProgramLST): 
                option = int(option)  # 1 based Menu Index
                ProgramLST[option-1].UserEntryPoint() # 0 based List Index
                ProgramLST[option-1].Update()
                for k,v in ProgramMenu_Items.items():
                    if k == (option): # 1 based Menu Index
                        ProgramMenu_Items[k] = [v[0],ProgramLST[option-1].installedStr] # append the new display string redraw menu
                        break
                ProgramMenu.Refresh(ProgramMenu_Items)
        except ValueError: # Maybe it was a letter passed and not an int
            for case in com.switch(option): # define only non program menu options I.E Letters TODO Maybe add a page function for longer lists?
                if case("e"): exit(0)
                
# Pythons built in main entrypoint
# calls init and runs main loop
if __name__ == "__main__":
	# Switch over to the main function
    main()