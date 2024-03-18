from netmiko import ConnectHandler
from auth import *
import re
import logging

#ipIntBrief = "show interface status | include Port | notconnect" #Real regex for production
#intNotConnPatt = r'(Gi|Te)\d+/\d+/\d+' #Real regex for production

# Regex patterns
searchPatt30d = r'output (\d{2}:\d{2}:\d{2})|output (\d+[ymwdhms]\d+[ymwdhms])'
intNotConnPatt = r'Et\d{1,2}\/\d{1,2}' #Used for tests
ipIntBrief = "show interface status | include Port | connect" #Used for tests

logging.basicConfig(filename='auth_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def notConnect(deviceIP, username, netDevice, printNotConnect=True, sshAccess=None):
    # This function is to show the interfaces not connected.
    # show interface status | include Port | notconnect
    try:
        if sshAccess is None:
            sshAccess = ConnectHandler(**netDevice)
            sshAccess.enable()
        
        shNotConnect = sshAccess.send_command(ipIntBrief)

        if 'Invalid input' in shNotConnect:
            raise ValueError("Invalid command")
        
        if printNotConnect:
            print(shNotConnect)
        
        logging.info(f"User {username} connected to {deviceIP} ran the command '{ipIntBrief}'\n")

        intNotConnected = re.findall(intNotConnPatt, shNotConnect)
        return intNotConnected

    except Exception as error:
        logging.error(f"User {username} connected to {deviceIP} tried to run '{ipIntBrief}', error message: {error}\n")
        return []
    finally:
        if sshAccess:
            sshAccess.disconnect()

def sh30dIntOff(deviceIP, username, netDevice):
        # This function is to show the interfaces not operating for more than 30 days
    # show interface g1/0/1
    # It will capture the string "output HH:MM:SS | y:m:d", that is, 
    # hours:minutes:second and years:months:days

    """
    Note: if you see the error output: Error: 'NoneType' object has no attribute 'group'
    please check if the output of "show interface e0/1" is "output never", if it's like this
    it will fail, it will only look for "output HH:MM:SS | y:m:d"
    """
    try:
        sshAccess = ConnectHandler(**netDevice)
        sshAccess.enable()

        intNotConnected = notConnect(deviceIP, username, netDevice, printNotConnect=False)
        
        for int in intNotConnected:
            cliCommand = f"show interface {int}"
            cliOutput = sshAccess.send_command(cliCommand)
            notConnectOutputBr = re.search(searchPatt30d, cliOutput)

            if notConnectOutputBr:
                notConnectOutputBr = notConnectOutputBr.group()
                logging.info(f"User {username} connected to {deviceIP} successfully found interfaces {int} not running " \
                             "for more than 30 days")

                timeToDays = 0
                timeUnit = re.findall(r'\d+[ymd]', notConnectOutputBr) 
                for unit in timeUnit:
                    num = int(unit[:-1])
                    if 'y' in unit:
                        timeToDays += num * 365
                    elif 'm' in unit:
                        timeToDays += num * 30
                    elif'w' in unit:
                        timeToDays += num * 7
                    else:
                        timeToDays += num
                    
                if timeToDays >= 30:
                    print("The interface",int, "was used",notConnectOutputBr,"ago")

            else:
                raise ValueError(f"Output line not found for interface {int}")
    except Exception as error:
        logging.error(f"User {username} connected to {deviceIP} couldn't find interfaces not running" \
                       f"for more than 30 days, error message: {error}")
    finally:
        if sshAccess:
            sshAccess.disconnect()