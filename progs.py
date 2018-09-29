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

# um O_e
def _IsInstalled(_progname):
    """Checks to see if a program is installed or not"""
    status = subprocess.getstatusoutput("dpkg-query -W -f='${Status}' " + _progname) # TODO https://www.tecmint.com/difference-between-apt-and-aptitude/
    if not status[0]:
        return True
    else:
        return False

# Install Object
# Atributes
#   _progname_ = ""
# Methods
#   _IsInstalled(self)
#   _DoInstall(self)
#   _Uninstall(self)
#   run(start_params)
#

def RunSubProc(*args):
        """Run Subprocess and catch exeptions"""
        try:
            retcode = call(args, shell=False)
            if retcode < 0:
                print("Child was terminated by signal", -retcode, file=sys.stderr)
            else:
                print("Child returned", retcode, file=sys.stderr)
        except OSError as e:
            print("Execution failed:", e, file=sys.stderr)

def Upgrade(sudopass=""):
    """Run Environmental upgrade"""
    RunSubProc("echo {} | sudo -S  aptitude -y update".format(sudopass))
    RunSubProc("echo {} | sudo -S  aptitude -y upgrade".format(sudopass))
    
class Program(object):
    """Defines a program that can be manipulated"""
    def __init__(self, name="", srvcname="",sudopass=""):
        """"Initilize object"""
        if MyOSType == "win32":
            print("Sorry Windows is not supported at this time :( we are working on it we promise.")
            #exit(1) # exit return failure to shell
            self.ProgName = name
            self._servicename_ = srvcname
            self.INSTALLED = _IsInstalled(self.ProgName)
            self.installedStr = self._frmtStr()
            self._sudo_ = "echo {} | sudo -S".format(sudopass)
        else:
            # set variables and init stuff
            self.ProgName = name
            self._servicename_ = srvcname
            self.INSTALLED = _IsInstalled(self.ProgName)
            self.installedStr = self._frmtStr()
            self._sudo_ = "echo {} | sudo -S".format(sudopass)

    def UserEntryPoint(self):
        """not sure what goes here yet"""
        print("{} object {} {}".format(self.ProgName,"Said","Hello"))

    def _frmtStr(self):
        """Return a print ready true/false green/red"""
        _strEnd_ = "{}{}".format(self.INSTALLED,com.color.END)
        if self.INSTALLED:
            return "{}{}".format(com.color.OKGREEN,_strEnd_)
        else:
            return "{}{}".format(com.color.FAIL,_strEnd_)

    def Install(self):
        """"Install package on system"""
        RunSubProc('{} aptitude --purge remove -y '+ self.ProgName)

    def _serviceUp(self):
        """Start service"""
        _ctlStartCMD_ = "{} systemctl start {}.service".format(self._sudo_,self._servicename_)
        _ctlEnableCMD_ = '{} systemctl enable {}.service'.format(self._sudo_,self._servicename_)
        RunSubProc(_ctlStartCMD_)
        RunSubProc(_ctlEnableCMD_)

    def _serviceDown(self):
        """Start service"""
        _ctlStopCMD_ = "{} systemctl stop {}.service".format(self._sudo_,self._servicename_)
        RunSubProc(_ctlStopCMD_)

    def _serviceRestart(self):
        """Start service"""
        _ctlRestartCMD_ = "{} systemctl retart {}.service".format(self._sudo_,self._servicename_)
        RunSubProc(_ctlRestartCMD_)
        return

    def Purge(self):
        """"Purge package from system"""
        if ProgramMenu.Confirm('Are you sure you want to remove {} from your machine.\nYou can always reinstall it later.'.format(self.ProgName)):
            RunSubProc('{} aptitude --purge remove -y {}'.format(self._sudo_,self.ProgName))
            self.INSTALLED = False

    def _gitConfig_():
        gname = input('What name would you like to use?: ')
        RunSubProc('git config --global user.name "{}"'.format(name)) # TODO what is this for?

####################################################  END CLASS ####################################################

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