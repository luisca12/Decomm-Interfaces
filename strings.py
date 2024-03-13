import os
from auth import *

def greeting():
        os.system("CLS")
        print("Welcome to the automated port removal program \n")

def menu(deviceIP, username):
        os.system("CLS")
        print("Connected to:", deviceIP, "as", username)
        print('\n  -------------------------------------------------------------- ')
        print('>      1. Show not connected interfaces                           <')
        print('>      2. Show interfaces not running for more than 30 days         <')
        print('>      3. Decom interfaces not running for more than 30 days       <')
        print('\n  -------------------------------------------------------------- ')

def inputError():
        os.system("CLS")
        print('  ------------------------------------------------- ')  
        print('>      INPUT ERROR: Only numbers are allowed       <')
        print('  ------------------------------------------------- ')

def log():
    with open('auth_log.txt', 'a') as text:
        text.write(f"Failed to login - Device IP: {deviceIP}, Username: {username}\n")