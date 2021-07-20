import mcUUID
import os

class MergeStatsMode():
    ONLINE2OFFLILE = "Online2Offlile"
    OFFLINE2ONLINE = "Offline2Online"

def fetchUUID(mode):
    playerList = mcUUID.getPlayerList(mode)
    print("Got {} items".format(len(playerList)))
    playerListData = {}
    print("Fetching UUID")
    # Fetch both offline and online uuid
    for playerName in playerList:
        playerListData[playerName] = {}
        playerListData[playerName]["OffineUUID"] = mcUUID.getOfflineUUID(playerName)
        playerListData[playerName]["OnineUUID"] = mcUUID.getOnlineUUID(playerName)
    return playerListData

def mergeStatsData(fileAPath, fileBPath):
    statsData1 = mcUUID.loadJsonFromFile(fileAPath)
    statsData2 = mcUUID.loadJsonFromFile(fileBPath)
    mergedData = statsData2
    for i in statsData1["stats"]:
        if (i not in statsData2["stats"].keys()):
            mergedData["stats"][i] = statsData1["stats"][i]
        else:
            for j in statsData1["stats"][i]:
                if (j not in statsData2["stats"][i].keys()):
                    mergedData["stats"][i][j] = statsData1["stats"][i][j]
                else:
                    mergedData["stats"][i][j] = statsData1["stats"][i][j] + statsData2["stats"][i][j]
    return mergedData

def mergeStats(worldName = "world", 
            mergeMode = MergeStatsMode().ONLINE2OFFLILE, 
            uuideMode = mcUUID.PlayerListReadMode().WHITELIST):
    targetPath = "./merged/stats"
    worldPath = "./{}".format(worldName)
    playerList = fetchUUID(uuideMode)
    if (mergeMode == MergeStatsMode().ONLINE2OFFLILE):
        for i in playerList:
            fileAPath = "{}/stats/{}.json".format(worldPath, playerList[i]["OnineUUID"])
            fileBPath = "{}/stats/{}.json".format(worldPath, playerList[i]["OffineUUID"])
            if (os.path.isfile(fileAPath) and os.path.isfile(fileBPath)):
                mergedData = mergeStatsData(fileAPath, fileBPath)
            elif (os.path.isfile(fileAPath)):
                mergeData = mcUUID.loadJsonFromFile(fileAPath)
            elif (os.path.isfile(fileBPath)):
                mergeData = mcUUID.loadJsonFromFile(fileBPath)
            else:
                print("Warning: Cant find any data with {}".format(i))
                continue
            mcUUID.saveJsonToFile("{}/{}.json".format(targetPath, playerList[i]["OffineUUID"]), mergedData)
    elif (mergeMode == MergeStatsMode().OFFLINE2ONLINE):
        pass
        # TODO
    else:
        print("Error: Undefined mode!")
        return
    if (not os.path.isdir("./merged/stats")):
        os.makedirs("./merged/stats")
    
mergeStats(uuideMode = mcUUID.PlayerListReadMode().USER_CACHE)