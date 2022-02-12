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
import os, npyscreen

####################################################################################
class Config(object):
    """Configuration Object
    Unleash your inner ini"""
    def __init__(self, file=""):
        self._file_ = file
        self.conf = ConfigParser()
        self.conf.read(os.path.abspath(self._file_))
        self.conf.sections()

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

# End class Config(object):

####################################################################################

class CollectiveTheme(npyscreen.Themes.ThemeManagers.ThemeManager):
    """Define a custom Theme and set default colors"""
#      BLACK_WHITE
#      BLACK_ON_DEFAULT
#      WHITE_ON_DEFAULT
#      BLUE_BLACK
#      CYAN_BLACK
#      GREEN_BLACK
#      MAGENTA_BLACK
#      RED_BLACK
#      YELLOW_BLACK
#      BLACK_RED
#      BLACK_GREEN
#      BLACK_YELLOW
#      BLACK_CYAN
#      BLUE_WHITE
#      CYAN_WHITE
#      GREEN_WHITE
#      MAGENTA_WHITE
#      RED_WHITE
#      YELLOW_WHITE
    default_colors = {
        'DEFAULT'     : 'RED_BLACK',
        'FORMDEFAULT' : 'GREEN_BLACK',
        'NO_EDIT'     : 'BLUE_BLACK',
        'STANDOUT'    : 'CYAN_BLACK',
        'CURSOR'      : 'WHITE_BLACK',
        'CURSOR_INVERSE': 'BLACK_WHITE',
        'LABEL'       : 'BLUE_BLACK',
        'LABELBOLD'   : 'YELLOW_BLACK',
        'CONTROL'     : 'GREEN_BLACK',
        'WARNING'     : 'RED_BLACK',
        'CRITICAL'    : 'BLACK_RED',
        'GOOD'        : 'GREEN_BLACK',
        'GOODHL'      : 'GREEN_BLACK',
        'VERYGOOD'    : 'BLACK_GREEN',
        'CAUTION'     : 'YELLOW_BLACK',
        'CAUTIONHL'   : 'BLACK_YELLOW',
        }

# End class CollectiveTheme(npyscreen.Themes.ThemeManagers.ThemeManager):

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
class TestApp(npyscreen.NPSApp):
	def main(self):
		# These lines create the form and populate it with widgets.
		# A fairly complex screen in only 8 or so lines of code - a line for each control.
		npyscreen.setTheme(CollectiveTheme)
		F = npyscreen.ActionFormWithMenus(name = "Collective Industries Installer",)
		ms2= F.add(npyscreen.TitleMultiSelect, max_height=10, value = [1,], name="Software Packages", 
				values = ["GitHub","GCC","CIFS","SSH","MariaDB","Apache","D2U","MC"], scroll_exit=True)
		
		# This lets the user play with the Form.
		F.edit()
class CI_Installer(npyscreen.NPSApp):
    def main():
        """Menu Builder framework"""

if __name__ == "__main__":
	App = TestApp()
	App.run()

####################################################################################