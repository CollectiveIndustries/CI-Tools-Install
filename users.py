import getpass
import progs

# User Object
class MyUser():
    """Defines a User Object"""
    def __init__(self):
        self.UserName = ""
        self.PassWord = ""

    def Login(self):
        """just initilize values"""
        self.UserName = getpass.getuser().replace(',', '')
        print("Please login to continue.\nUsername = {}".format(self.UserName))
        self.PassWord = getpass.getpass("Login Password: ") # TODO #9 Check users login info and reask if wrong
        progs.RunSudoProc('ls -shal /tmp 2>&1 /dev/null')