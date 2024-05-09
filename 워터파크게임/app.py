from ursina import *


app = Ursina()



Map = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
     

]
x = 0
y = 5
z = 0

def start():
    
    for z in range(len(Map)):
        for x in range(len(Map[0])):
            block = Entity(model='cube', color=color.green, texture='white_cube', scale=3)
            block.x = x * 3
            block.z = z * 3
            Map[z][x] = block


def update():
    global x, z
    x += held_keys["d"] * 0.1
    x -= held_keys["a"] * 0.1
    z -= held_keys["w"] * 0.1
    z += held_keys["s"] * 0.1
    camera.x = x
    camera.y = y
    camera.z = z
    camera.rotation.z = 180


start()

app.run()