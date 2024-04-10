from auth import *
from strings import *
from functions import *
from commandsCLI import *
import os

def main():
    greetingString()
    deviceIP, username, netDevice = Auth()
    intChosen = None

    while True:
        print("* Only numbers are accepted *")
        menuString(deviceIP, username), print("\n")
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
                    selectIntOff(deviceIP, username, netDevice)

            elif selection == "4":
                    delIntOff(deviceIP, username, netDevice)
                # This function is to delete the interfaces that we want to decom
            
            elif selection == "5":
                shDelIntOff()
                # This function is to show the interfaces modified

            elif selection == "6":
                print("Exiting the program...\n")
                os.system("PAUSE")
                authLog.info(f"User {username} connected to device IP {deviceIP} successfully logged out")
                break   
        else:
            # inputErrorString will print that an invalid option was choen
            inputErrorString()
            os.system("PAUSE")

if __name__ == "__main__":
    main()