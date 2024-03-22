import re
import logging
from log import *

def checkIsDigit(input_str):
    authLog.info(f"Option from the menu successfully validated, option: {input_str}")
    return input_str.strip().isdigit()
    #if input_str.strip().isdigit():
    #    return True
    #else:
    #    return False

def validateIP(deviceIP):
    validIP_Pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    if re.match(validIP_Pattern, deviceIP):
        authLog.info(f"\nIP successfully validated{deviceIP}")
        return all(0 <= int(num) <= 255 for num in deviceIP.split('.'))
    return False

def validateInt(userInput):
    validInt_Pattern = r'\b(?:Et|Gi|Te)\d+\/\d+(?:\/\d+)?(?:-\d+)?(?:,\s*(?:Et|Gi|Te)\d\/\d+(?:\/\d+)?(?:-\d+)?)*\b'
    authLog.info(f"Interface successfully validated {userInput}")
    return bool(re.fullmatch(validInt_Pattern, userInput))