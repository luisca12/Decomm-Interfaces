import re

def validateIP(deviceIP):
    validIP_Pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    if re.match(validIP_Pattern, deviceIP):
        return all(0 <= int(num) <= 255 for num in deviceIP.split('.'))
    return False