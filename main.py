from auth import *
from strings import *
from functions import *
from commandsCLI import *
import os

greeting()
#deviceIP, username, netDevice = Auth()

while True:
    print("* Only numbers are accepted *")
    menu(deviceIP, username), print("\n")
    selection = input("Please choose the option that you want: ")
    if checkIsDigit(selection):
        if selection == "1":
            # This option will show the interfaces not connected.
            notConnect(deviceIP, username, netDevice)
        
        elif selection == "2":
            # This function will show the interfaces not operating for more than 30 days
                sh30dIntOff(deviceIP, username, netDevice)
        
        elif selection == "3":
            # This function is to select the interfaces that we want to decom
                selectIntOffTest()

        elif selection == "4":
            # This function is to delete the interfaces that we want to decom
             continue
    else:
        inputError()
        os.system("PAUSE")