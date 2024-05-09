from easiersocket import Server

app = Server("127.0.0.1", 22222)
def get_protocol_1(data):
    print(data)
    app.send("p2", "Wow! Great! ")
app.add_protocol("p1", get_protocol_1)
app.run()
