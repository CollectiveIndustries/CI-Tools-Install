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

# System Imports
import time
import users

# Custom Imports
from lib import com
from menu import BuildMenu

###############
## Variables ##
###############
DELAY = 2
global usr

# Build Objecs
MyOS = com._OS_()
usr = users.MyUser()

######################################################################

##############
##Functions ##
##############

# Debug function
# TODO #12 Debug --> Verbosity
# Turns debug function into a verbosity logger
# should be usable for providing diffrent log
# levels for debugging, errors, info, etc
def Debug(var1, var2, TF):
    """Debug Function"""
    DEBUG = True # flip de switch >..<
    if DEBUG == True and TF == True: #
        print(var1 +' = ' + var2)

######################################################################


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
    main()
