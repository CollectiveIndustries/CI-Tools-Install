#!/usr/bin/python3

######################################
##									##
##		Collective Industries		##
##		 	   Classes				##
##									##
##		  By: Levi & Andrew			##
##				©2018				##
######################################

#############
## Imports ##
#############

#################
## Main Script ##
#################
def git_install():
	gname = input('What name would you like to use?: ')
	if(oper == 'debian'):
		os.system('sudo apt-get -y update')
		os.system('sudo apt-get -y upgrade')
		os.system('sudo apt-get -y install git')
		os.system('git config --global user.name "',gname,'"')
	else:
		print("Sorry Windows is not supported at this time :( we are working on it we promise.")
		
def gcc_install():
	if(oper == 'debian'):
		os.system('sudo apt-get -y update')
		os.system('sudo apt-get -y upgrade')
		os.system('sudo apt-get install -y build-essential')
	else:
		print("Sorry Windows is not supported at this time :( we are working on it we promise.")
		
def cifs_install():
	if(oper == 'debian'):
		os.system('sudo apt-get -y update')
		os.system('sudo apt-get -y upgrade')
		os.system('sudo apt-get install -y cifs-utils')
	else:
		print("Sorry Windows is not supported at this time :( we are working on it we promise.")
		
def ssh_install():
	if(oper == 'debian'):
		os.system('sudo apt-get -y update')
		os.system('sudo apt-get -y upgrade')
		os.system('sudo apt-get -y install openssh-server')
		os.system('sudo systemctl start ssh.service')
		os.system('sudo systemctl enable ssh.service')
	else:
		print("Sorry Windows is not supported at this time :( we are working on it we promise.")
		
#class mysql_install():
	
	
#class mdb_install():
	
	
#class apache_install():
	
	
#class d2u_install():
	
	
def ip_config():
	if(oper == 'debian'):
		nic = raw_input('Are you wanting to setup your WiFi or your Eithernet? [W/E]: ')
	if nic.lower() == 'w':
		# Setting up WiFi IP 
		cname = raw_input('What is the name of your WiFi Adapter? [wlan0]: ')
		if cname == '':
			cname = 'wlan0'
		else:
			cname = cname			
	if nic.lower() == 'e':
		# Setting up Ethernet IP
		cname = raw_input('What is the name of your Eithernet Adapter? [eth0]: ')
		if cname == None:
			cname = 'eth0'
			with fileinput.FileInput('/etc/network/interfaces', implace=True, backup='.bak') as file:
				for line in file:
					print(line.replace(cname, 'replacement text'))
		else:
			cname = cname
	else:
		print("Sorry Windows is not supported at this time :( we are working on it we promise.")
	