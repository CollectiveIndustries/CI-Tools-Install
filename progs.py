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
from subprocess import call
import re, menu

###############
## Variables ##
###############
MyOS = com._OS_()
MyOSType = MyOS._type_

# Install Object
# Atributes
#   _progname_ = ""
# Methods
#   _IsInstalled(self)
#   _DoInstall(self)
#   _Uninstall(self)
#   Go(start_params)
#

class installer():
    def _git_():
        gname = input('What name would you like to use?: ')
        if(MyOSType == 'debian'):
            _dinstall_('git')
            call('git config --global user.name "',gname,'"')
        else:
            print("Sorry Windows is not supported at this time :( we are working on it we promise.") # TODO 4 little

    def _gcc_():
        if(MyOSType == 'debian'):
            _dinstall_('build-essential')
        else:
            print("Sorry Windows is not supported at this time :( we are working on it we promise.") # TODO 3 little

    def _cifs_():
        if(MyOSType == 'debian'):
            _dinstall_('cifs-utils')
        else:
            print("Sorry Windows is not supported at this time :( we are working on it we promise.") # TODO 2 little

    def _ssh_():
        if(MyOSType == 'debian'):
            _dinstall_('openssh-server')
            call('sudo systemctl start ssh.service') # TODO build a service handler (we want more then one service to be stop/start/restart
            call('sudo systemctl enable ssh.service')
        else:
            print("Sorry Windows is not supported at this time :( we are working on it we promise.") # TODO 1 little

    def _mysql_():
        if(MyOSType == 'debian'):
            _dinstall('mysql-server')
        else:
            print("Sorry Windows is not supported at this time :( we are working on it we promise.")# TODO 5 little >..<
    
    def _mdb_():
        if(MyOSType == 'debian'):
            _dinstall_('mariadb-server')
        else:
            print("Sorry Windows is not supported at this time :( we are working on it we promise.") # TODO O_e 6? little
    
    def apache_install():
        if(MyOSType == 'debian'):
            _dinstall_('apache2')
        else:
            print("Sorry Windows is not supported at this time :( we are working on it we promise.") # TODO OMG 7 LITTLE

    def d2u_install():
        if(MyOSType == 'debian'):
            _dinstaller('dos2unix')
        else:
            print("Sorry Windows is not supported at this time :( we are working on it we promise.") # ~_~ why do i even? 8 little

def _dinstall_(program): # Installaion for Debian
    call ("sudo aptitude -y update")
    call ("sudo aptitude -y upgrade")
    call ("sudo aptitude -y "+ program)

def uninstall(_prog_):
    call('sudo aptitude --purge remove -y '+ _prog_)

def install_check(prog, num):
    if ProgramMenu_Items[num][2] == 'Installed':
        if ProgramMenu.Confirm('Are you sure you want to remove {} from your machine.\nYou can always Reinstall it later.'.format(ProgramMenu_Items["1"][1])):
            uninstall(prog)
        else:
            main()
    else:
        time.sleep(DELAY)
        installer._$prog_
        print('Installation Successful')
        main()

def ip_config():
    # TODO Refactor with menu class setup refuse empty and defualts
    if(MyOSType == 'debian'):
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