from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoAuthenticationException
from netmiko.exceptions import NetMikoTimeoutException
from validateIP import validateIP
import socket

deviceIP = 0
username = ""
execPrivPassword = ""
netDevice = {}

def Auth():
    global deviceIP
    global username
    global execPrivPassword
    global netDevice
    while True:
        deviceIP = input("Please enter the device IP: ")
        if validateIP(deviceIP):
            break
        else:
            print("Invalid IP address format. Please enter a valid IP address.")

    while True:
        username = input("Please enter your unsername: ")
        password = input("Please enter your password: ")
        execPrivPassword = input("Pleae input your enable password: ")

        netDevice = {
            'device_type' : 'cisco_ios',
            'ip' : deviceIP,
            'username' : username,
            'password' : password,
            'secret' : execPrivPassword
        }

        try:
            sshAccess = ConnectHandler(**netDevice)
            sshAccess.enable()
            print("Login successful! \n")

            with open('auth_log.txt', 'a') as text:
                text.write(f"Successful login - Device IP: {deviceIP}, Username: {username}\n")
            break

        except NetMikoAuthenticationException:
            print("\n Login incorrect. Please check your username and password")
            print(" Retrying operation... \n")
            with open('auth_log.txt', 'a') as text:
                text.write(f"Failed to login - Device IP: {deviceIP}, Username: {username}\n")

        except NetMikoTimeoutException:
            print("\n Connection to the device timed out. Please check your network connectivity and try again.")
            print(" Retrying operation... \n")
            with open('auth_log.txt', 'a') as text:
                text.write(f"Connection timed out, device not reachable - Device IP: {deviceIP}, Username: {username}\n")

        except socket.error:
            print("\n IP address is not reachable. Please check the IP address and try again.")
            print(" Retrying operation... \n")
            with open('auth_log.txt', 'a') as text:
                text.write(f"Device unreachable - Device IP: {deviceIP}, Username: {username}\n")

    return deviceIP, username, netDevice