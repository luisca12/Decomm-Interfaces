from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoAuthenticationException, NetMikoTimeoutException
from validateIP import validateIP
import socket

deviceIP = ""
username = ""
execPrivPassword = ""
netDevice = {}

def Auth():
    global deviceIP, username, execPrivPassword, netDevice
    
    while True:
        deviceIP = input("Please enter the device IP: ")
        if validateIP(deviceIP):
            try:
                reachTest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                reachTest.settimeout(3)
                reachResult = reachTest.connect_ex((deviceIP, 22))
                if reachResult == 0:
                    print("Device is reachable on port TCP 22.")
                else:
                    print("Device is not reachable on port TCP 22.\n")
                    continue
            except Exception as error:
                print("Error occured while checking device reachability:", error)
                continue
            break
        else:
            print("Invalid IP address format. Please enter a valid IP address.")

    while True:
        try:
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

            sshAccess = ConnectHandler(**netDevice)
            sshAccess.enable()
            print("Login successful! \n")

            with open('auth_log.txt', 'a') as text:
                text.write(f"Successful login - Device IP: {deviceIP}, Username: {username}\n")

            return deviceIP, username, netDevice

        except NetMikoAuthenticationException:
            print("\n Login incorrect. Please check your username and password")
            print(" Retrying operation... \n")
            with open('auth_log.txt', 'a') as text:
                text.write(f"ERROR: Failed to login - Device IP: {deviceIP}, Username: {username}\n")

        except NetMikoTimeoutException:
            print("\n Connection to the device timed out. Please check your network connectivity and try again.")
            print(" Retrying operation... \n")
            with open('auth_log.txt', 'a') as text:
                text.write(f"ERROR: Connection timed out, device not reachable - Device IP: {deviceIP}, Username: {username}\n")
            
        except socket.error:
            print("\n IP address is not reachable. Please check the IP address and try again.")
            print(" Retrying operation... \n")
            with open('auth_log.txt', 'a') as text:
                text.write(f"ERROR: Device unreachable - Device IP: {deviceIP}, Username: {username}\n")   