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
import subprocess

def Debug(var1, var2, TF):
	DEBUG = True
	if DEBUG == True and TF == True:
		print(var1 +' = ' + var2)	
		
def init():
	subprocess.call('clear')
	if platform == 'linux' or platform == 'linux2':
		# linux
		with open('/etc/os-release') as file:
			global oper
			oper = file.readlines()
			oper = oper[5].split('=')
			oper = oper[1]
			
def main():
	init()
	Debug('oper', oper, True)
	if oper == 'debian':
		print('Running Debian OS')
			
main()	
