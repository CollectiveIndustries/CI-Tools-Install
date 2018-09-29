#! /usr/bin/python

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
		
def init():
	os.system('clear')
	if platform == 'linux' or platform == 'linux2':
		# linux
		with open('/etc/os-release') as file:
			global oper
			oper = file.readlines()
			oper = oper[5].split('=')
			oper = oper[1].strip()
			
def main():
	init()
	Debug('oper', oper, True)
	if oper == 'debian':
		os.system('sudo apt-get -y update')
		os.system('sudo apt-get -y upgrade')
		os.system('sudo apt-get -y install git')
		print('Running Debian OS')
			
main()	
