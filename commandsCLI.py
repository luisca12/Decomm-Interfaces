import os
from netmiko import ConnectHandler
from auth import *
import re

ipIntBrief = "show interface e0/1 r"
searchPatt30d = r'output (\d{2}:\d{2}:\d{2})|output (\d+[ymwdhms]\d+[ymwdhms])'

def notConnect(deviceIP, username, netDevice):
    # This function is to show the interfaces not connected.
    # show interface status | include Port | notconnect
    try:
        sshAccess = ConnectHandler(**netDevice)
        sshAccess.enable()
        
        shNotConnect = sshAccess.send_command(ipIntBrief)

        if 'Invalid input' in shNotConnect:
            raise ValueError("Invalid command")
        
        with open('auth_log.txt', 'a') as text:
            text.write(f"INFO: user {username} with device IP {deviceIP} ran the command '{ipIntBrief}'\n")

        return shNotConnect

    except Exception as error:
        print(f"Error: {error}\n")
        with open('auth_log.txt', 'a') as text:
            text.write(f"ERROR: user {username} with device IP {deviceIP} tried to run '{ipIntBrief}', error message: {error}\n")
    return None

def sh30dIntOff(deviceIP, username, netDevice):
    # This function is to show the interfaces not operating for more than 30 days
    # show interface g1/0/1
    # It will capture the string "output HH:MM:SS | y:m:d", that is, 
    # hours:minutes:second and years:months:days
    try:
        sshAccess = ConnectHandler(**netDevice)
        sshAccess.enable()
        
        notConnectOutput = notConnect(deviceIP, username, netDevice)
        notConnectOutputBr = re.search(searchPatt30d, notConnectOutput)

        if notConnectOutput:
            notConnectOutputBr = notConnectOutputBr.group()
            with open('auth_log.txt', 'a') as text:
                text.write(f"INFO: user {username} with device IP {deviceIP} sucessfully found interfaces not running " \
                            "for more than 30 days\n")
                print(notConnectOutputBr)
        else:
            raise ValueError("Output line not found")
    except Exception as error:
        print(f"Error: {error}\n")
        with open('auth_log.txt', 'a') as text:
            text.write(f"ERROR: user {username} with device IP {deviceIP} couldn't find interfaces not running" \
                       f"for more than 30 days, error message: {error}\n")    