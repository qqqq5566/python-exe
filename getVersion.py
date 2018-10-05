import configparser
import requests
from json import loads
from os import path

def getVersion():
    respone = requests.get("http://api.chain-bar.com/api/version-version/windows")
    data = loads(respone.text)

    if data['success']:
        return data['version']
    else:
        return None


def readLocalIniFile():
    if path.exists("updateConfig.ini"):
        config = configparser.ConfigParser()
        config.read("updateConfig.ini")
        return config.get("Version", "Version")
    else:
        return False


def getDiff():
    version = readLocalIniFile()
    reVersion = getVersion()
    if version != None and reVersion != None:
       if(version == reVersion):
           return False
       else:
           return True

if __name__ == '__main__':
    print(getDiff())