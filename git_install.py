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

from sys import platform
import os

def Debug(var1, var2, TF):
	DEBUG = True
	if DEBUG == True and TF == True:
		print(var1 +' = ' + var2)
		
def GetOS():
    _SystemOS_ = platform.strip()
    Debug("startup(): _SystemOS_",_SystemOS_,True)

    if (_SystemOS_ == 'linux' or _SystemOS_ == 'linux2'):
    # linux
        with open('/etc/os-release') as file:
            oper = file.readlines()
            oper = oper[5].split('=')
            return oper[1].strip() # Grab OS release Name we want to know what flavor of lenny we use.
    elif(_SystemOS_ == 'win32'):
        return _SystemOS_

def main():
    oper = GetOS()
    Debug('oper', oper, True)
    if(oper == 'debian'):
        os.system('sudo apt-get -y update')
        os.system('sudo apt-get -y upgrade')
        os.system('sudo apt-get -y install git')
        print('Running Debian OS')
    else:
        print("Sorry Windows is not supported at this time :( we are working on it we promise.")

main()	
