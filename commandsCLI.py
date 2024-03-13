import os
from netmiko import ConnectHandler
from auth import *

ipIntBrief = "show ip interface brief"

def notConnect(deviceIP, username, netDevice):
    # This function is to show the interfaces not connected.
    # show interface status | include Port | notconnect
    # this variable will return me this
    try:
        sshAccess = ConnectHandler(**netDevice)
        sshAccess.enable()
        
        shNotConnect = sshAccess.send_command(ipIntBrief)
        print(shNotConnect)

        if 'Invalid input' in shNotConnect:
            raise ValueError("Invalid command")

    except Exception as error:
        print(f"Error: {error}\n")
        with open('auth_log.txt', 'a') as text:
            text.write(f"ERROR: user {username} with device IP {deviceIP} tried to run '{ipIntBrief}', error message: {error}\n")

def runInt():
    # Used to show the unused interfaces for more than 30 days
    return 0

def delRunInt():
    # Usted to remove the configuration of the unused interfaces
    return 0