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
from lib import com
from shutil import which
from progs import Program
import os, pwd, time, subprocess, sys

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

###############
## Main Menu ##
###############
def main_menu():
    MyOS.Clear()  
    print('')
    print ('Installations')
    print ('1. GitHub ............... ', is_tool('git'))
    print ('2. GCC .................. ', is_tool('build-essential'))
    print ('3. CIFS Filesystem ...... ', is_tool('cifs-utils'))
    print ('4. SSH Server ........... ', is_tool('openssh-server'))
    print ('5. MySQL Server ......... ', is_tool('mysql-server'))
    print ('6. MariaDB Server ....... ', is_tool('mariadb-server'))
    print ('7. Apache ............... ', is_tool('apache2'))
    print ('8. Dos 2 Unix Converter . ', is_tool('dos2unix'))
    print ('9. Midnight Commander ... ', is_tools('mc'))
    print ('')
    print ('Configurations')
    #print ('8. Set IP to Static/Dynamic')
    #print ('9. Config 2')
    print ('')
    print ('E. Exit')
    print ('')

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