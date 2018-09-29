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
import subprocess
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
#   run(start_params)
#


class Program(object):
    """Defines a program that can be manipulated"""
    def __init__(self, name="", sername=""):
        if MyOSType == "win32":
            print("Sorry Windows is not supported at this time :( we are working on it we promise.")
            exit(1) # exit return failure to shell
        else:
            # set variables and init stuff
            self._progname_ = name
            self._servicename_ = sername
            self.INSTALLED = self._IsInstalled()

    def _IsInstalled(self):
        """Checks to see if a program is installed or not"""
        status = subprocess.getstatusoutput("dpkg-query -W -f='${Status}' " + self._progname_) # TODO https://www.tecmint.com/difference-between-apt-and-aptitude/
        if not status[0]:
            return True
        else:
            return False

    def _RunSubProc(self,*args):
        """Run Subprocess and catch exeptions"""
        try:
            retcode = call(self._progname_ + args, shell=False) # TODO https://www.tecmint.com/difference-between-apt-and-aptitude/
            if retcode < 0:
                print("Child was terminated by signal", -retcode, file=sys.stderr)
            else:
                print("Child returned", retcode, file=sys.stderr)
        except OSError as e:
            print("Execution failed:", e, file=sys.stderr)

    def Install(self):
        """"Install package on system"""
        subprocess.call('sudo aptitude --purge remove -y '+ self._progname_) # TODO https://www.tecmint.com/difference-between-apt-and-aptitude/ Use _RunSubProc(self, ARGS)

    def _serviceUp(self):
        """Start service"""
        subprocess.call('sudo systemctl start ssh.service') # TODO Use _RunSubProc(self, ARGS)
        subprocess.call('sudo systemctl enable ssh.service')# TODO Use _RunSubProc(self, ARGS)

    def _serviceDown(self):
        """Start service"""
        return
    def _serviceRestart(self):
        """Start service"""
        return

    def Purge(self):
        """"Purge package from system"""
        if ProgramMenu.Confirm('Are you sure you want to remove {} from your machine.\nYou can always Reinstall it later.'.format(self._progname_)):
            subprocess.call('sudo aptitude --purge remove -y '+ self._progname_) # TODO https://www.tecmint.com/difference-between-apt-and-aptitude/
            self.INSTALLED = False

    def _gitConfig_():
        gname = input('What name would you like to use?: ')
        if(MyOSType == 'debian'):
            call('git config --global user.name "',gname,'"')
        else:

def _dinstall_(program): # Installaion for Debian
    call("sudo aptitude -y update", shell=False)
    call("sudo aptitude -y upgrade", shell=False)
    call("sudo aptitude -y "+ program, shell=False) # TODO not exactly sure what were doing here?

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

def word_search(file, _oldWord, _newWord): # TODO maybe a regex? idk what we're doing here
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