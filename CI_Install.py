#! /usr/bin/python

from sys import platform
from subprocess import Popen, PIPE
import distutils.spawn
import os
import subprocess
import getpass

user = getpass.getuser()

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
        
    print ('######################')
    print ('##                  ##')
    print ('##   CI INSTALLER   ##')
    print ('##                  ##')
    print ('######################')
    
    print ('Welcome ' + user + '. What would you like to install?')
    
    print ('1. GitHUB      - ' + str(prog_check('github')))
    print ('2. GCC       - ' + str(prog_check('gcc')))
    print ('3. Teamspeak - ' + str(prog_check('teamspeak')))
