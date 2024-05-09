import json




data = {
    "Players" : [],


}





def new_connect(data):
    dictdata = json.dumps(data)

    data["Players"].append(dictdata)



def playerleavemap(data):
    PlayerUUID = [playerin["UUID"] for playerin in data["Players"]]

    for i, Uuid in enumerate(PlayerUUID):
        if data["UUID"] == Uuid:
            del data["Players"][i]

def updateplayerdata(data):
    PlayerUUID = [playerin["UUID"] for playerin in data["Players"]]

    for i, Uuid in enumerate(PlayerUUID):
        if data["UUID"] == Uuid:
            data["Player_In_Map"].append(data["Players"][i]) 
def getdata():
    return data
    