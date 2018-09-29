import getpass
# User Object
class MyUser():
    """Defines a User Object"""
    def __init__(self):
        self.UserName = ""
        self.PassWord = ""

    def Login(self):
        """just initilize values"""
        self.UserName = getpass.getuser().replace(',', '')
        print("Please login to continue.\nUsername=".format(self.UserName))
        self.PassWord = getpass.getpass("Login Password: ")