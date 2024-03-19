import re
import logging

logging.basicConfig(filename='auth_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def checkIsDigit(input_str):
    return input_str.strip().isdigit()
    logging.info(f"String successfully validated{input_str}")
    #if input_str.strip().isdigit():
    #    return True
    #else:
    #    return False

def validateIP(deviceIP):
    validIP_Pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    if re.match(validIP_Pattern, deviceIP):
        return all(0 <= int(num) <= 255 for num in deviceIP.split('.'))
    return False

def validateInt(userInput):
    validInt_Pattern = r'\b(?:Et|Gi|Te)\d+\/\d+(?:\/\d+)?(?:-\d+)?(?:, (?:Et|Gi|Te)\d\/\d+(?:\/\d+)?(?:-\d+)?)*\b'
    return bool(re.fullmatch(validInt_Pattern, userInput))