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
	print oper
	if oper == 'debian':
		print('Running Debian OS')
			
main()	
