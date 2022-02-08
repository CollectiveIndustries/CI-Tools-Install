#!/usr/bin/python3

#############################
##  Collective Industries  ##
##          Tools          ##
##                         ##
##    By: Levi & Andrew    ##
##          ©2018          ##
#############################

###############
##  Imports  ##
###############
from configparser import ConfigParser
import os

####################################################################################
class Config(object):
    """Configuration Object
    Unleash your inner ini"""
    def __init__(self, file=""):
        self._file_ = file
        self.conf = ConfigParser()
        self.conf.read(os.path.abspath(self._file_))
        self.conf.sections()

####################################################################################

## Config Parse Helper ##

    def MapSection(self,section):
        dict1 = {}
        options = self.conf.options(section)
        for option in options:
            try:
                dict1[option] = self.conf.get(section, option)
                if dict1[option] == -1:
                    print("Skipping: %s %s" % (section,option))
            except:
                print("Exception on %s %s!" % (section,option))
                dict1[option] = None
        return dict1

## Config section writter ##
    def AddSection(self,section):
        """Add a new [SECTION] Header to the INI Config"""
        self.conf.add_section(section)
    
    def SetValue(self,section,key,value):
        """Add a new KEY=VALUE pair to the config under [SECTION]"""
        self.conf.set(section,key,value)
    
    def Write(self):
        """Write the Configuration settings to the disk"""
        cfgfile = open(self._file_, "wb")
        self._file_.write(cfgfile)
        cfgfile.close()

####################################################################################


################
## Variables  ##
################
MainConfigFile = "config.d/main.cfg"

######################
##  Object Classes  ##
######################
ConfigSettings = Config(MainConfigFile)

# Global Configuration Settings
GITHUB_PROG_NAME = ConfigSettings.MapSection("GitHub")['prog_name']
GITHUB_DESC = ConfigSettings.MapSection("GitHub")['desc']
GCC_PROG_NAME = ConfigSettings.MapSection("GCC")['prog_name']
GCC_DESC = ConfigSettings.MapSection("GCC")['desc']
CIFS_PROG_NAME = ConfigSettings.MapSection("CIFS")['prog_name']
CIFS_DESC = ConfigSettings.MapSection("CIFS")['desc']
SSH_PROG_NAME = ConfigSettings.MapSection("SSH")['prog_name']
SSH_DESC = ConfigSettings.MapSection("SSH")['desc']
SSH_PORT = ConfigSettings.MapSection("SSH")['port']
SSH_KEY = ConfigSettings.MapSection("SSH")['public_key']
MARIA_PROG_NAME = ConfigSettings.MapSection("MariaDB")['prog_name']
MARIA_DESC = ConfigSettings.MapSection("MariaDB")['desc']
MARIA_PORT = ConfigSettings.MapSection("MariaDB")['port']
MARIA_USER = ConfigSettings.MapSection("MariaDB")['user_name']
APACHE_PROG_NAME = ConfigSettings.MapSection("Apache")['prog_name']
APACHE_DESC = ConfigSettings.MapSection("Apache")['desc']
D2U_PROG_NAME = ConfigSettings.MapSection("D2U")['prog_name']
D2U_DESC = ConfigSettings.MapSection("D2U")['desc']
MC_PROG_NAME = ConfigSettings.MapSection("MC")['prog_name']
MC_DESC = ConfigSettings.MapSection("MC")['desc']

####################################################################################

###############
## Main Menu ##
###############

def BuildMenu():
    """Menu Builder framework"""
    print('')

####################################################################################

