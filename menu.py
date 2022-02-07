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
from lib import config
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

