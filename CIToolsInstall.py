######################################
##									##
##		Collective Industries		##
##		 Tools Installation			##
##									##
##		  By: Levi & Andrew			##
##				©2018				##
######################################


#############
## Imports ##
#############
import os
import pwd
import getpass

###############
## Variables ##
###############
user = if pwd.getpwuid(os.getuid())[4] != ""
		print(pwd.getpwuid(os.getuid())[4])
	   else:
	    print(getpass.getuser()) #Gets users full name. If full name is blank then uses username.

os_name	= os.name
os_plat = platform.linux_distribustion()
bit = platform.machine()

##############
##Functions ##
##############
def working(yn)
	if yn = "y"
		print("Working")
	else:
		print("Not Working")
		
##########
## Menu ##
##########
print("Welcome ",users," to the Collective Industries Tools Installation.")
print ("Please select what program(s) you would like to install.")
print("")
print("")
print("1.Program 1 .... ") working("n")
print("2.Program 2 .... ") working("n")
print("3.Program 3 .... ") working("n")