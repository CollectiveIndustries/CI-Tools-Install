#! /usr/bin/python
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
from sys import platform
from subprocess import Popen, PIPE
import distutils.spawn
import os
import subprocess
import getpass
import pwd
import getpass

###############
## Variables ##
###############
user = pwd.getpwuid(os.getuid())[4]
uname = getpass.getuser()
os_name	= os.name

def prog_check(program):
	p = Popen(['which', program], stdout=PIPE, stderr=PIPE)
	p.communicate()
	prog = p.returncode == 0
	if prog == 1:
		return 'Installed'
	else:
		return 'Not Installed'
		
if platform == "linux" or platform == "linux2":
    # linux    
    with open('/etc/os-release') as file:
        oper = file.readlines()
        oper = oper[5].split('=')
        oper = oper[1]

if uname == '':
	users = user
else:
	users = uname
	
def main():
	print ('######################')
	print ('##                  ##')
	print ('##   CI INSTALLER   ##')
	print ('##                  ##')
	print ('######################')
 
	print("Welcome " + users + " to the Collective Industries Tools Installation.")
	print ("Please select what program(s) you would like to install.")
	print("")
	print("")
	print ('1. GitHUB    - ' + str(prog_check('git')))
	print ('2. GCC       - ' + str(prog_check('gcc')))
	print ('3. Teamspeak - ' + str(prog_check('teamspeak')))
	
	choice = input('Choice: ')
	
	if choice == '1':
		git()
		
def git():
	# GitHub Installation
	subprocess.call('clear')
	print('This is were the github installation function will go')
	
main()
