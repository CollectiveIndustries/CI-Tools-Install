# User Object
class MyUser():
    """Defines a User Object"""
    def __init__(self):
        self.UserName = ""
        self.PassWord = ""

    def GetPasswrd(self):
        """just initilize values"""
        self.UserName = getpass.getuser().replace(',', '')
        self.PassWord = getpass.getpass("Login Password: ")