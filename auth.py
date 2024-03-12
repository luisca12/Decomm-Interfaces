from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoAuthenticationException
import validateIP

def Auth():
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
            break
        except NetMikoAuthenticationException:
            print("\n Login incorrect. Please check your username and password")
            print(" Retrying operation... \n")

Auth()