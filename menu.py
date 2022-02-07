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

################
## Variables  ##
################
ConfigFile = "config.d/menu.cfg"
conf = ConfigParser()
conf.read(os.path.abspath(ConfigFile))
conf.sections()


## Config Parse Helper ##

def ConfigSectionMap(section):
    dict1 = {}
    options = conf.options(section)
    for option in options:
        try:
            dict1[option] = conf.get(section, option)
            if dict1[option] == -1:
                print("Skipping: %s %s" % (section,option))
        except:
            print("Exception on %s %s!" % (section,option))
            dict1[option] = None
    return dict1

## Config section writter ##
def ConfigAddSection(section):
	conf.add_section(section)

def ConfigSetValue(section,key,value):
	conf.set(section,key,value)

def ConfigWrite():
	cfgfile = open(ConfigFile, "wb")
	conf.write(cfgfile)
	cfgfile.close()

class Menu_Settings:
    
    GITHUB_PROG_NAME = ConfigSectionMap("GitHub")['prog_name']
    GITHUB_DESC = ConfigSectionMap("GitHub")['desc']

    GCC_PROG_NAME = ConfigSectionMap("GCC")['prog_name']
    GCC_DESC = ConfigSectionMap("GCC")['desc']

    CIFS_PROG_NAME = ConfigSectionMap("CIFS")['prog_name']
    CIFS_DESC = ConfigSectionMap("CIFS")['desc']

    SSH_PROG_NAME = ConfigSectionMap("SSH")['prog_name']
    SSH_DESC = ConfigSectionMap("SSH")['desc']
    SSH_PORT = ConfigSectionMap("SSH")['port']
    SSH_KEY = ConfigSectionMap("SSH")['public_key']
    
    
    MARIA_PROG_NAME = ConfigSectionMap("MariaDB")['prog_name']
    MARIA_DESC = ConfigSectionMap("MariaDB")['desc']
    MARIA_PORT = ConfigSectionMap("MariaDBB")['port']
    MARIA_USER = ConfigSectionMap("MariaDB")['user']


    APACHE_PROG_NAME = ConfigSectionMap("Apache")['prog_name']
    APACHE_DESC = ConfigSectionMap("Apache")['desc']
    
    D2U_PROG_NAME = ConfigSectionMap("D2U")['prog_name']
    D2U_DESC = ConfigSectionMap("D2U")['desc']
        
    MC_PROG_NAME = ConfigSectionMap("MC")['prog_name']
    MC_DESC = ConfigSectionMap("MC")['desc']