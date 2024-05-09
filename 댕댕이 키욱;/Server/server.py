from easiersocket import Server
import json




data = {
    "Players" : [],


}





def new_connect(data):
    dictdata = json.loads(data)

    data["Players"].append(dictdata)
    app.send("message", json.dumps({"target" : dictdata["name"]}))


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
    


app = Server("127.0.0.1", 22222)       



app.add_protocol("new_connect", new_connect)
app.add_protocol("playerleavemap", playerleavemap)
app.add_protocol("updateplayerdata", updateplayerdata)

def loop(data):
    app.send(getdata())

app.add_protocol("loop", loop)

