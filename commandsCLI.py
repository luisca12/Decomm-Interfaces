from netmiko import ConnectHandler
from log import *
from strings import *
from auth import *

import re

shRun = "show run"
intChosen = ""
decomIntCLIOutput = []
intNotConnected = []
interfaceList30Day = []

# Regex patterns
ipIntBrief = "show interface status | include Port | notconnect" #Real regex for production
intNotConnPatt = r'[a-zA-Z]+\d+\/(?:\d+\/)*\d+' #Real regex for production
searchPatt30d = r'output (\d{2}:\d{2}:\d{2})|output (\d+[ymwdhms]\d+[ymwdhms])|output never'
intChosenPatt = r'/\b(?:Et|Gi|Te|Tw)\d+\/\d+(?:\/\d+)?(?:-\d+)?(?:, (?:Et|Gi|Te|Tw)\d\/\d+(?:\/\d+)?(?:-\d+)?)*\b'

# intNotConnPatt = r'Et\d{1,2}\/\d{1,2}\/\{1,2}\' #Used for tests
# ipIntBrief = "show interface status | include Port|connected" #Used for tests

def notConnect(deviceIP, username, netDevice, printNotConnect=True, sshAccess=None):
    # This function is to show the interfaces not connected.
    # show interface status | include Port | notconnect
    global intNotConnected
    try:
        if sshAccess is None:
            with ConnectHandler(**netDevice) as sshAccess:
                sshAccess.enable()

                shNotConnect = sshAccess.send_command(ipIntBrief)

                if 'Invalid input' in shNotConnect:
                    raise ValueError("Invalid command")
                
                if printNotConnect:
                    print(shNotConnect)
                
                authLog.info(f"User {username} connected to {deviceIP} ran the command '{ipIntBrief}'\n")

                intNotConnected = re.findall(intNotConnPatt, shNotConnect)
                return intNotConnected

    except Exception as error:
        print(f"An error occurred: {error}")
        authLog.error(f"User {username} connected to {deviceIP} tried to run '{ipIntBrief}', error message: {error}\n")
        authLog.debug(traceback.format_exc())
        return []
    finally:
        os.system("PAUSE")

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
    global interfaceList30Day
    with ConnectHandler(**netDevice) as sshAccess:
        try:
            sshAccess.enable()
            for interface in intNotConnected:
                cliCommand = f"show interface {interface}"
                cliOutput = sshAccess.send_command(cliCommand)
                notConnectOutputBr = re.search(searchPatt30d, cliOutput)

                if notConnectOutputBr:
                    notConnectOutputBr = notConnectOutputBr.group()

                    if notConnectOutputBr != 'output never':
                        
                        authLog.info(f"User {username} connected to {deviceIP} successfully found interfaces {interface} not running " \
                            "for more than 30 days")

                        timeToDays = 0
                        timeUnit = re.findall(r'\d+[ymwd]', notConnectOutputBr) 
                        for unit in timeUnit:
                            num = int(unit[:-1])
                            if 'y' in unit:
                                timeToDays += num * 365
                            elif 'm' in unit:
                                timeToDays += num * 30
                            elif 'w' in unit:
                                timeToDays += num * 7
                            else:
                                timeToDays += num
                            
                        if timeToDays >= 30:
                            interfaceList30Day.append(interface)
                            print(f"The interface {interface} was used {timeToDays} days ago")
                            showInterface = f"show run int {interface} | begin interface"
                            showInterfaceOut = sshAccess.send_command(showInterface)
                            print(f"{showInterfaceOut}")
                        else:
                            print("Interface has been running",notConnectOutputBr)
                    else:
                        print(f"Skipping interface {interface} as its last output is: {notConnectOutputBr}")
                        continue 
                else:
                    raise ValueError(f"The interface {interface} last output: {notConnectOutputBr}")
        except Exception as error:
            print(f"An error occurred: {error}")
            authLog.error(f"User {username} connected to {deviceIP} couldn't find interfaces not running " \
                f"for more than 30 days, error message: {error}")
            authLog.debug(traceback.format_exc())
        finally:
            print(f"Summary of the interfaces not running for more than 30 days:\n{interfaceList30Day}")
            os.system("PAUSE")
    return interfaceList30Day

def selectIntOff(deviceIP, username, netDevice):
    # This function is to select the interfaces that we want to decom
    # This is manually input by the network operator
    global intChosen

    try:
        with ConnectHandler(**netDevice) as sshAccess:

            while True:
                selIntString()    
                intChosen = input("Interfaces: ")

                # validateInt is a boolean function
                intChosenOut = validateInt(intChosen)

                if intChosenOut:
                    print("Interfaces properly entered and saved. \n")
                    authLog.info(f"User {username} connected to {deviceIP} successfully selected the interfaces to decom:" \
                        f"{intChosen}")
                    return intChosen
                
                else:
                    print(f"Invalid input \"{intChosen}\"\n")
                    authLog.error("The return value from the function validateInt is False (incorrect), please check the interfaces chosen.")
                    os.system("PAUSE")
                
    except Exception as error:
        print(f"An error occurred: {error}")
        authLog.error(f"User {username} connected to {deviceIP} encountered an error while validating input:{error}")
        authLog.debug(traceback.format_exc())
                    
    finally:
        os.system("PAUSE")

def delIntOff(deviceIP, username, netDevice):
    # This function is to go thorught the several interfaces and decomm them
    try:
        global decomIntCLIOutput
        if intChosen:
            with ConnectHandler(**netDevice) as sshAccess:

                shRunString(deviceIP)
                shRunOutput = sshAccess.send_command(shRun)
                configChangeLog.info(f"Automation ran the command \"{shRun}\" into the deviceIP {deviceIP} "\
                    f"before making the changes successfully:\n{shRunOutput}")

                print(f"\nInterfaces selected for decommissioning: {intChosen}")
                print("Will now begin to decommission the interfaces.\n")

                intModified = intChosen.split(",")
                for interface in intModified:
                    print("Processing interface: ",interface)
                    configChangeLog.info(f"Configuring interface {interface}\n{decomIntCLI(interface)}\n")
                    
                    sshAccess.send_config_set(decomIntCLI(interface))
                    decomIntCLIOutput.append(sshAccess.send_config_set(decomIntCLI(interface)))

                    configChangeLog.info(f"User {username} successfully connected to device IP {deviceIP} and ran the following commands:\n {decomIntCLI(interface)}\n")
                    authLog.info(f"User {username} connected to device IP {deviceIP} successfully, processed and configured the interface {intChosen} in VLAN 1001.")
                    print("Successfully decommissioned the interfaces.")
                    
                shRunOutput = sshAccess.send_command(shRun)
                configChangeLog.info(f"Automation ran the command \"{shRun}\" into the deviceIP {deviceIP} "\
                    f"after making the changes successfully:\n{shRunOutput}")
                return decomIntCLIOutput
                    
        else:
            print("No interfaces selected. Please go back to option 3\n")
            authLog.warning(f"User {username} connected to {deviceIP} did not select any interfaces for decommissioning.")
            return []
                
    except Exception as error:
        print(f"An error occurred: {error}")
        authLog.error(f"User {username} connected to {deviceIP} encountered an error while processing interfaces for decommissioning: {error}")

    finally:
        os.system("PAUSE")

def decomIntCLI(interface):
    decomIntCLI = [
            f"interface range {interface}",
            "description unusedPort",
            "switchport mode access",
            "switchport access vlan 1001",
            "shutdown"
    ]
    return decomIntCLI

def decomIntList(interface):
    decomIntList = [
            f"interface {interface}",
            "description unusedPort",
            "switchport mode access",
            "switchport access vlan 1001",
            "shutdown"
    ]
    return decomIntList

def autoChooseInt(deviceIP, username, netDevice):
        try:
            if interfaceList30Day:
                with ConnectHandler(**netDevice) as sshAccess:
                    sshAccess.enable()
                    shRunString(deviceIP)
                    with open(f"{deviceIP}_Outputs.txt", "a") as file:
                        file.write(f"User {username} connected to device IP {deviceIP}\n\n")
                        shRunOutputBefore = sshAccess.send_command(shRun)
                        configChangeLog.info(f"Automation ran the command \"{shRun}\" into the deviceIP {deviceIP} "\
                                    f"before making the changes successfully:\n{shRunOutputBefore}")
                        file.write("INFO: Taking show run before the changes\n")
                        file.write(f"{shRunOutputBefore}\n\n")
                        print(f"\nInterfaces selected for decommissioning: {interfaceList30Day}")
                        print("Will now begin to decommission the interfaces.\n")
                        os.system("PAUSE")
                        file.write("INFO: Starting the configuration changes")
                        # for interface in interfaceList30Day:
                        #     print("Processing interface: ",interface)
                        #     configChangeLog.info(f"Configuring interface {interface}:\n{decomIntList(interface)}\n")  
                        #     file.write(f"INFO: Configuring interface {interface}\n")

                        #     decomOut = sshAccess.send_config_set(decomIntList(interface))
                        #     decomIntCLIOutput.append(decomOut)

                        #     file.write(f"INFO: Successfully configured the interface: \n{decomOut}\n\n")
                        #     configChangeLog.info(f"User {username} successfully connected to device IP {deviceIP} and ran the following commands:\n {decomIntCLI(interface)}\n")
                        #     authLog.info(f"User {username} connected to device IP {deviceIP} successfully, processed and configured the interface {intChosen} in VLAN 1001.")
                        #     print("Successfully decommissioned the interfaces.")

                        file.write(f"\n\nINFO: Taking show run after the changes\n")  
                        shRunOutAfter = sshAccess.send_command(shRun)
                        file.write(f"{shRunOutAfter}")
                        configChangeLog.info(f"Automation ran the command \"{shRun}\" into the deviceIP {deviceIP} "\
                            f"after making the changes successfully:\n{shRunOutAfter}")
                        return decomIntCLIOutput       
            else:
                print("No interfaces selected. Please go back to option 2\n")
                authLog.warning(f"User {username} connected to {deviceIP} did not select any interfaces for decommissioning.")
                return []
                    
        except Exception as error:
            print(f"An error occurred: {error}")
            authLog.error(f"User {username} connected to {deviceIP} encountered an error while processing interfaces for decommissioning: {error}")
            authLog.debug(traceback.format_exc())

        finally:
            os.system("PAUSE")



def shDelIntOff():
    shDelIntOffString()
    for output in decomIntCLIOutput:
        print(output)
    os.system("PAUSE")