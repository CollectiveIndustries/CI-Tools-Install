#!/usr/bin/env python
#coding:utf8

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
user = pwd.getpwuid(os.getuid())[4]
uname = getpass.getuser()
os_name	= os.name
os_plat = platform.linux_distribustion()
bit = platform.machine()
		
##############
##Functions ##
##############
		
##########
## Menu ##
##########
print("Welcome ",users," to the Collective Industries Tools Installation.")
print ("Please select what program(s) you would like to install.")
print("")
print("")
print("1.Program 1 .... Not Working") 
print("2.Program 2 .... Not Working") 
print("3.Program 3 .... Not Working") 