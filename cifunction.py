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
from lib import com
import re
###############
## Variables ##
###############
MyOS =com._OS_()
oper = MyOS._type_

#################
## Main Script ##
#################
def word_search(file, word, rword):
    _file1_ = open(file, 'r')
    _file2_ = open(file, 'w')
    #count = 0
    #for line in _file_:
    #    count = count + 1
    #    if re.match('(.*)'+word+'(.*)', line):
            #print (line,)
    for line in _file1_:
        _file1_.write(line.replace(word, rword))
        _file1_.close()
        
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
		
def mysql_install():
    if(oper == 'debian'):
        os.system('sudo apt-get -y update')
        os.system('sudo apt-get -y upgrade')
        os.system('sudo apt-get install -y mysql-server')
    else:
        print("Sorry Windows is not supported at this time :( we are working on it we promise.")	
	
def mdb_install():
    if(oper == 'debian'):
        os.system('sudo apt-get -y update')
        os.system('sudo apt-get -y upgrade')
        os.system('sudo apt-get install -y mariadb-server')
    else:
        print("Sorry Windows is not supported at this time :( we are working on it we promise.")
	
	
def apache_install():
    if(oper == 'debian'):
        os.system('sudo apt-get -y update')
        os.system('sudo apt-get -y upgrade')
        os.system('sudo apt-get install -y apache2')
    else:
        print("Sorry Windows is not supported at this time :( we are working on it we promise.")
	
def d2u_install():
    if(oper == 'debian'):
        os.system('sudo apt-get -y update')
        os.system('sudo apt-get -y upgrade')
        os.system('sudo apt-get install -y dos2unix')
    else:
        print("Sorry Windows is not supported at this time :( we are working on it we promise.")	
	
def ip_config():
    if(oper == 'debian'):
        nic = input('Are you wanting to setup your WiFi or your Eithernet? [W/E]: ')
    if nic.lower() == 'w':
		# Setting up WiFi IP 
        cname = input('What is the name of your WiFi Adapter? [wlan0]: ')
        _sdip_ = input('Would you like a Static IP or a Dynamic IP? [S/D]: ')
        if cname == '':
            cname = 'wlan0'
            if _sdip_.lower() == 's':
                word_search('/etc/network/interfaces', cname+' inet dhcp', cname+'inet static')
            else:
                word_search('/etc/network/interfaces', cname+' inet static', cname+'inet dhcp')
        else:
            print('good')
            cname = cname			
        if nic.lower() == 'e':
            # Setting up Ethernet IP
            cname = input('What is the name of your Eithernet Adapter? [eth0]: ')
        if cname == None:
            cname = 'eth0'
            with fileinput.FileInput('/etc/network/interfaces', implace=True, backup='.bak') as file:
                for line in file:
                    print(line.replace(cname, 'replacement text'))
        else:
            cname = cname
    else:
        print("Sorry Windows is not supported at this time :( we are working on it we promise.")
	