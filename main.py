from auth import *
from strings import *
from functions import *
from commandsCLI import *
import os

greeting()
deviceIP, username, netDevice = Auth()

while True:
    print("* Only numbers are accepted *")
    menu(deviceIP, username), print("\n")
    selection = input("Please choose the option that you want: ")
    if checkIsDigit(selection):
        if selection == "1":
            notConnect(deviceIP, username, netDevice)
            os.system("PAUSE")
            break
        else:
            print("Not coded yet")
            break
    else:
        inputError()
        os.system("PAUSE")