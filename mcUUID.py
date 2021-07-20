import hashlib
import json
import os
import urllib.request

class PlayerListReadMode():
    WHITELIST = "whitelist"
    USER_CACHE = "usercache"

def loadJsonFromFile(filePath):
    with open(filePath, 'r') as f:
        return json.load(f)
        
def saveJsonToFile(filePath, jsonObject):
    with open(filePath, 'w') as f:
        json.dump(jsonObject, f, ensure_ascii = False, indent = 4)
        
def getData(url):
    response = urllib.request.urlopen(url)
    return response.read()

def getJavaUUID(uuid):
    return "{}-{}-{}-{}-{}".format(uuid[:8], uuid[8:12], uuid[12:16], uuid[16:20], uuid[20:])

def getOnlineUUID(playerName):
    try:
        data = getData("https://api.mojang.com/users/profiles/minecraft/{}".format(playerName))
        data = json.loads(data)
        return getJavaUUID(data["id"])
    except:
        return None

def getOfflineUUID(playerName):
    playerName = "OfflinePlayer:{}".format(playerName)
    hashedPlayerName = str(hashlib.md5(playerName.encode("utf-8")).hexdigest())
    charArray = []
    for i in range(0, len(hashedPlayerName), 2):
        charArray.append(chr(int(hashedPlayerName[i:i + 2], 0x10)))
    charArray[6] = chr(ord(charArray[6]) & 0x0f | 0x30) # set uuid version to 3
    charArray[8] = chr(ord(charArray[8]) & 0x3f | 0x80)
    playerUUID = ""
    for i in range(len(charArray)):
        playerUUID += "{:0^2}".format(hex(ord(charArray[i]))[2:])
    return getJavaUUID(playerUUID)
    
def getPlayerList(mode = None):
    if (mode == PlayerListReadMode().WHITELIST):
        filename = "{}.json".format(PlayerListReadMode().WHITELIST)
    elif (mode == PlayerListReadMode().USER_CACHE):
        filename = "{}.json".format(PlayerListReadMode().USER_CACHE)
    else:
        print("Error: Undefined mode!")
        return None
    cache = loadJsonFromFile(filename)
    playerList = []
    for items in cache:
        playerList.append(items["name"])
    return playerList
    

def getPlayerListFromUserCache():
    return getPlayerList(PlayerListReadMode().USER_CACHE)

def getPlayerListFromWhitelist():
    return getPlayerList(PlayerListReadMode().WHITELIST)
    
getPlayerListFromWhitelist()