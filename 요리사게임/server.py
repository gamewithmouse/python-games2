from easiersocket import Server
import json
app = Server("127.0.0.1", 22222)
player_list = {}

def player_info(data):
    data_d = json.loads(data.split("|")[0])
    player_list[data_d["name"]] = data_d
    app.send("Players", json.dumps(player_list) + "|")
    

def New_Connect(data):
    print(data)
    data_d = json.loads(data.split("|")[0])
    player_list[data_d["name"]] = {
        "Name": data_d["name"]
        ,"X": 0
        ,"Y": 0}
    
app.add_protocol("new_connect", New_Connect)
app.add_protocol("player_info", player_info)

if __name__ == "__main__":
    app.run()
