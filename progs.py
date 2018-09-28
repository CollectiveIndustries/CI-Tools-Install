######################################
##									##
##		Collective Industries		##
##		 	   Classes				##
##									##
##		  By: Levi & Andrew			##
##				©2018				##
######################################

# TODO rewrite progs module for use of the prefrered pythonic subprocess module
# In the official python documentation we can read that subprocess should be used
# for accessing system commands.
#
# https://docs.python.org/3/library/subprocess.html

#############
## Imports ##
#############
from lib import com
import re

###############
## Variables ##
###############
MyOS = com._OS_()
oper = MyOS._type_

#################
## Main Script ##
#################
def word_search(file, _oldWord, _newWord):
    _file1_ = open(file, 'r')
    _file2_ = open(file, 'w')
    #count = 0
    #for line in _file_:
    #    count = count + 1
    #    if re.match('(.*)'+word+'(.*)', line):
            #print (line,)
    for line in _file1_:
        _file1_.write(line.replace(_oldWord, _newWord))
        _file1_.close()
        
def git_install():
	gname = input('What name would you like to use?: ')
	if(oper == 'debian'):
		os.system('sudo apt-get -y update') # TODO refactor for subproccess
		os.system('sudo apt-get -y upgrade')# TODO refactor for subproccess
		os.system('sudo apt-get -y install git')
		os.system('git config --global user.name "',gname,'"')
	else:
		print("Sorry Windows is not supported at this time :( we are working on it we promise.") # TODO 4 little
		
def gcc_install():
	if(oper == 'debian'):
		os.system('sudo apt-get -y update') # TODO refactor for subproccess
		os.system('sudo apt-get -y upgrade')# TODO refactor for subproccess
		os.system('sudo apt-get install -y build-essential')
	else:
		print("Sorry Windows is not supported at this time :( we are working on it we promise.") # TODO 3 little
		
def cifs_install():
	if(oper == 'debian'):
		os.system('sudo apt-get -y update') # TODO refactor for subproccess
		os.system('sudo apt-get -y upgrade')# TODO refactor for subproccess
		os.system('sudo apt-get install -y cifs-utils')
	else:
		print("Sorry Windows is not supported at this time :( we are working on it we promise.") # TODO 2 little
		
def ssh_install():
	if(oper == 'debian'):
		os.system('sudo apt-get -y update') # TODO refactor for subproccess
		os.system('sudo apt-get -y upgrade')# TODO refactor for subproccess
		os.system('sudo apt-get -y install openssh-server')
		os.system('sudo systemctl start ssh.service') # TODO build a service handler (we want more then one service to be stop/start/restart
		os.system('sudo systemctl enable ssh.service')
	else:
		print("Sorry Windows is not supported at this time :( we are working on it we promise.") # TODO 1 little
		
def mysql_install():
    if(oper == 'debian'):
        os.system('sudo apt-get -y update') # TODO refactor for subproccess
        os.system('sudo apt-get -y upgrade')# TODO refactor for subproccess
        os.system('sudo apt-get install -y mysql-server') # TODO Oh and a service handler here
    else:
        print("Sorry Windows is not supported at this time :( we are working on it we promise.")# TODO 5 little >..<

def mdb_install():
    if(oper == 'debian'):
        os.system('sudo apt-get -y update') # TODO refactor for subproccess
        os.system('sudo apt-get -y upgrade')# TODO refactor for subproccess
        os.system('sudo apt-get install -y mariadb-server') # TODO Hey that service handler? yeah we need it here too
    else:
        print("Sorry Windows is not supported at this time :( we are working on it we promise.") # TODO O_e 6? little

def apache_install():
    if(oper == 'debian'):
        os.system('sudo apt-get -y update') # TODO refactor for subproccess
        os.system('sudo apt-get -y upgrade')# TODO refactor for subproccess
        os.system('sudo apt-get install -y apache2') # TODO hey wait a minute service handler?
    else:
        print("Sorry Windows is not supported at this time :( we are working on it we promise.") # TODO OMG 7 LITTLE

def d2u_install():
    if(oper == 'debian'):
        os.system('sudo apt-get -y update') # TODO refactor for subproccess
        os.system('sudo apt-get -y upgrade')# TODO refactor for subproccess
        os.system('sudo apt-get install -y dos2unix')
    else:
        print("Sorry Windows is not supported at this time :( we are working on it we promise.") # ~_~ why do i even? 8 little

def ip_config():
    # TODO Refactor with menu class setup refuse empty and defualts
    if(oper == 'debian'):
        nic = input('Are you wanting to setup your WiFi or your Eithernet? [W/E]: ')
    if nic.lower() == 'w':
		# Setting up WiFi IP 
        cname = input('What is the name of your WiFi Adapter? [wlan0]: ')
        _sdip_ = input('Would you like a Static IP or a Dynamic IP? [S/D]: ')
        if cname == '':
            cname = 'wlan0'
            if _sdip_.lower() == 's':
                # TODO wtf?
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
        print("Sorry Windows is not supported at this time :( we are working on it we promise.") # TODO OH COME ON!!!!!