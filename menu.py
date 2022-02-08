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
from lib import com
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

    def SectionMap(self,section):
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
MenuConfigFile = "config.d/main.cfg"

######################
##  Object Classes  ##
######################
Menu_Settings = Config(MenuConfigFile)

# Global Menu Options
GITHUB_PROG_NAME = Menu_Settings.SectionMap("GitHub")['prog_name']
GITHUB_DESC = Menu_Settings.SectionMap("GitHub")['desc']
GCC_PROG_NAME = Menu_Settings.SectionMap("GCC")['prog_name']
GCC_DESC = Menu_Settings.SectionMap("GCC")['desc']
CIFS_PROG_NAME = Menu_Settings.SectionMap("CIFS")['prog_name']
CIFS_DESC = Menu_Settings.SectionMap("CIFS")['desc']
SSH_PROG_NAME = Menu_Settings.SectionMap("SSH")['prog_name']
SSH_DESC = Menu_Settings.SectionMap("SSH")['desc']
SSH_PORT = Menu_Settings.SectionMap("SSH")['port']
SSH_KEY = Menu_Settings.SectionMap("SSH")['public_key']
MARIA_PROG_NAME = Menu_Settings.SectionMap("MariaDB")['prog_name']
MARIA_DESC = Menu_Settings.SectionMap("MariaDB")['desc']
MARIA_PORT = Menu_Settings.SectionMap("MariaDB")['port']
MARIA_USER = Menu_Settings.SectionMap("MariaDB")['user_name']
APACHE_PROG_NAME = Menu_Settings.SectionMap("Apache")['prog_name']
APACHE_DESC = Menu_Settings.SectionMap("Apache")['desc']
D2U_PROG_NAME = Menu_Settings.SectionMap("D2U")['prog_name']
D2U_DESC = Menu_Settings.SectionMap("D2U")['desc']
MC_PROG_NAME = Menu_Settings.SectionMap("MC")['prog_name']
MC_DESC = Menu_Settings.SectionMap("MC")['desc']

####################################################################################

###############
## Main Menu ##
###############

def BuildMenu():
    """Menu Builder framework"""
    print('')

####################################################################################

