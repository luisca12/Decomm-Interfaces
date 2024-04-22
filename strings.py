import os
from auth import *

def greetingString():
        os.system("CLS")
        print("Welcome to the automated port removal program \n")

def menuString(deviceIP, username):
        print(f"\nConnected to: {deviceIP} as {username}")
        print('\n  -------------------------------------------------------------- ')
        print("          Welcome to the automated port decomm program             ")
        print("       Please choose an option, only numbers are accepted          ")
        print('  -------------------------------------------------------------- ')
        print('>      1. Show not connected interfaces                            <')
        print('>      2. Show interfaces not running for more than 30 days        <')
        print('>      3. To auto choose AND decomm the interfaces                 <')
        print('>      4. To manually choose the interfaces to decom:              <')
        print('>      5. To manually decomm the interfaces not running 30 days +  <')
        print('>      6. Show the interfaces that were modified                   <')   
        print('>      7. To exit the program                                      <')     
        print('\n  -------------------------------------------------------------- ')

def inputErrorString():
        os.system("CLS")
        print('  ------------------------------------------------- ')  
        print('>      INPUT ERROR: Only numbers are allowed       <')
        print('  ------------------------------------------------- ')

def selIntString():
        print('  ------------------------------------------------- ')  
        print('>      Please input the interfaces to decom:       <')
        print('>    Example: Et0/1-10, Gi1/0/11-20, Te1/0/1-4     <')
        print('  ------------------------------------------------- ')

def shRunString(deviceIP):
        print('  ------------------------------------------------- ')  
        print(f'> Taking a show run of the device {deviceIP}    <')
        print('>\t   Please wait until it finishes\t  <')
        print('  ------------------------------------------------- ')
        os.system("\nPAUSE")

def shDelIntOffString():
        print('  ------------------------------------------------- ')  
        print('>  Below is the output of the interfaces modified  <')
        print('  ------------------------------------------------- ')