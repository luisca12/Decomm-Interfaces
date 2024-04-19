from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoAuthenticationException, NetMikoTimeoutException
from functions import *
from log import *
import socket
import os

deviceIP = ""
username = ""
execPrivPassword = ""
netDevice = {}

def Auth():
    global deviceIP, username, execPrivPassword, netDevice
    
    while True:
        deviceIP = input("Please enter the device IP: ")
        if validateIP(deviceIP):
            checkReachPort22(deviceIP)
            break
        else:
            print("Invalid hostname/IP address format. Please enter a valid hostname/IP address.")
    deviceIP, username, netDevice = requestLogin(deviceIP)

    return deviceIP,username,netDevice