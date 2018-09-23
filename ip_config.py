#! /usr/bin/python
#coding:utf8

######################################
##									##
##		Collective Industries		##
##	   SSH Server Installation		##
##									##
##		  By: Levi & Andrew			##
##				©2018				##
######################################

############
## Import ##
############
from sys import platform
import os

###############
## Functions ##
###############
# Debug function
def Debug(var1, var2, TF):
	DEBUG = True
	if DEBUG == True and TF == True:
		print(var1 +' = ' + var2)
		
# Determines what O/S you are running
def GetOS():
	_SystemOS_ = platform.strip()
	Debug("startup(): _SystemOS_",_SystemOS_,False)
	if (_SystemOS_ == 'linux' or _SystemOS_ == 'linux2'):
		# linux
		with open('/etc/os-release') as file:
			oper = file.readlines()
			oper = oper[5].split('=')
			return oper[1].strip() # Grab OS release Name we want to know what flavor of lenny we use.
	elif(_SystemOS_ == 'win32'):
		return _SystemOS_
		
# Determins out to clear your screen 
def OSClear(osname):
	if(osname == "win32"):
		os.system("cls")
	else: # well its not Windows we can just "clear"
		os.system("clear")
		
# Initial function	
def init():
	# Checks to see what O/S yor running and set the variable
	global oper
	oper = GetOS()
	return oper
	main()
	
def main():
	init()
	#Debug('oper', oper, False)
	oper = GetOS()	
	if(oper == 'debian'):
		nic = input('Are you wanting to setup your WiFi or your Eithernet? [W/E]: ')
		if nic.lower() == 'w':
			# Setting up WiFi IP 
			cname = input('What is the name of your WiFi Adapter? [wlan0]: ')
			if cname == '':
				cname = 'wlan0'
			else:
				cname = cname			
		if nic.lower() == 'e':
			# Setting up Ethernet IP
			cname = input('What is the name of your Eithernet Adapter? [eth0]: ')
			if cname == '':
				cname = 'eth0'
			else:
				cname = cname
	else:
		print("Sorry Windows is not supported at this time :( we are working on it we promise.")
		
main()
