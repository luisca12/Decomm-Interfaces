from auth import Auth
from strings import *
from functions import checkIsDigit
import os

greeting()
deviceIP, username = Auth()

while True:
    print("* Only numbers are accepted *")
    menu(deviceIP, username), print("\n")
    selection = input("Please choose the option that you want: ")
    if checkIsDigit(selection):
        if selection == "1":
            print("It is working")
            break
        else:
            print("Not coded yet")
            break
    else:
        inputError()
        os.system("PAUSE")