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
# https://docs.python.org/3/library/subprocess.html#popen-objects

#############
## Imports ##
#############
from fileinput import FileInput
from lib import com
from subprocess import Popen, PIPE
from menu import TextMenu
from shutil import which
import users, shlex, sys, subprocess, re

###############
## Variables ##
###############
MyOS = com._OS_()
MyOSType = MyOS._type_
usr = users.MyUser()

def RunSubProc(args): # TODO Exception: [WinError 2] The system cannot find the file specified Setup a "win32" test environment for debugging
        """Run Subprocess and catch exeptions"""
        try:
            p1 = Popen(shlex.split(args), stdout=PIPE)
            return p1.communicate()[0]
        except OSError as e:
            print("Execution failed:", e, file=sys.stderr)

# TODO fix sudo being called if already root
# set up a non blocking read so we can monitor output and provide user feedback on status https://eli.thegreenplace.net/2017/interacting-with-a-long-running-child-process-in-python/
def RunSudoProc(args): 
        """Run Subprocess with PIPE and catch exeptions
        Return output"""
        p1_arg = "echo {}".format(usr.PassWord)
        p2_arg = "sudo -S {}".format(args)
        try:
            p1 = Popen(shlex.split(p1_arg), stdout=PIPE)
            p2 = Popen(shlex.split(p2_arg), stdin=p1.stdout, stdout=PIPE)
            p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
            return p2.communicate()[0]
        except OSError as e:
            print("Execution failed:", e, file=sys.stderr)

def Upgrade():
    """Run Environmental upgrade"""
    print("Preparing system for new package..............")
    RunSudoProc("aptitude -y update")
    RunSudoProc("aptitude -y upgrade")

# Program Object
# Atributes
#   str ProgName
#   bool INSTALLED
#   str installedStr -- red/green not/installed formated string
#
#
# Methods
#   __init__                initilizes Atributes
#   Install(self)           Install Program
#   Purge(self)             Remove program and cleanup
#   _serviceDown(self)      If prog comes with a service this turns it off AND disables it (maybe we can change that?)
#   _serviceRestart(self)   If prog comes with a service Restarts it
#   _serviceUp(self)        If prog comes with a service Starts AND Enables it (maybe we can change that?)
#   _gitConfig_()           # TODO this doesnt really belong in ALL the program objects. not sure where this goes yet.

class Program(object):
    """Defines a program that can be manipulated"""
    def __init__(self, name="", srvcname=""):
        """"Initilize object"""
        if MyOSType == "win32":
            print("Sorry Windows is not supported at this time :( we are working on it we promise.")
            #exit(1) # exit return failure to shell Following options are for DEBUG in win32 ONLY
            self.ProgName = name
            self._servicename_ = srvcname
            self.INSTALLED = self._is_installed()
            self.installedStr = self._frmtStr()
        else:
            # set variables and init stuff
            self.ProgName = name
            self._servicename_ = srvcname
            self.INSTALLED = self._is_installed()
            self.installedStr = self._frmtStr()
    def Update(self):
        """Updates Program object with values"""
        self.INSTALLED = self._is_installed()
        self.installedStr = self._frmtStr()

    def is_tool(name):
        """Check whether `name` is on PATH and marked as executable."""
        program = which(name)
        if program == None:
            install_check = "Not Installed"
        else:
            install_check = "Installed" 
        return install_check

    def UserEntryPoint(self):
        """not sure what goes here yet"""
        if self.INSTALLED: 
            self.Purge()
        else:
            Upgrade()
            self.Install()
        #print("{} object {} {}".format(self.ProgName,"Said","Hello"))

    def _AptParse_(self,results=b''):
        """Parse the results from apt return status
        see man aptitude for more details on package status"""
        tmpStr = results.decode() # asume utf-8 and decode
        LineArray = tmpStr.split(sep='\n') # Parse each line into an array (list)
        item_lst = []
        del LineArray[-1] # None of that >..<
        for line in LineArray:
            item_lst = line.split(maxsplit=3)
            if self.ProgName == item_lst[1]: 
                return item_lst[0]

    def _frmtStr(self):
        """Return a print ready true/false green/red"""
        _strEnd_ = "{}".format(com.color.END)
        if self.INSTALLED:
            return "{}Installed{}".format(com.color.OKGREEN,_strEnd_)
        else:
            return "{}Not Installed{}".format(com.color.FAIL,_strEnd_)

    def Install(self):
        """"Install package on system"""
        RunSudoProc('aptitude install -y '+ self.ProgName)
        self.Update()

    def _serviceUp(self):
        """Start service"""
        _ctlStartCMD_ = "systemctl start {}.service".format(self._servicename_)
        _ctlEnableCMD_ = 'systemctl enable {}.service'.format(self._servicename_)
        RunSudoProc(_ctlStartCMD_)
        RunSudoProc(_ctlEnableCMD_)

    def _serviceDown(self):
        """Start service"""
        _ctlStopCMD_ = "{} systemctl stop {}.service".format(self._sudo_,self._servicename_)
        RunSubProc(_ctlStopCMD_)

    def _serviceRestart(self):
        """Start service"""
        _ctlRestartCMD_ = "systemctl retart {}.service".format(self._servicename_)
        RunSudoProc(_ctlRestartCMD_)
        return

    def Purge(self):
        """"Purge package from system"""
        if TextMenu.Confirm('You are about to remove {} from your machine.\nYou can always reinstall it later.'.format(self.ProgName),''):
            RunSudoProc('aptitude remove -y {}'.format(self.ProgName))
            self.INSTALLED = False
            self.Update()

    def _gitConfig_():
        gname = input('What name would you like to use?: ')
        RunSubProc('git config --global user.name "{}"'.format(gname)) # TODO See Progs comment box ^

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
                with FileInput.FileInput('/etc/network/interfaces', implace=True, backup='.bak') as file:
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