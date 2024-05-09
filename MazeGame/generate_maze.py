import random



import datetime

import math

import os

random.seed(str(datetime.datetime.today()))




MAZE_WALL = "a"

MAZE_EMPTY = "b"

MAZE_END = "e"

MAZE_SHOP = "s"

MAZE_MONEY = "m"

def generate_maze(width, height):
    maze = generate_wall_board(width, height)

    has_end = False
    
    for x in range(0, width):
        for y in range(0, height):
            if x % 2 == 1 and y % 2 == 1:

                
                
                maze[y][x] = MAZE_EMPTY
                if random.randint(0, 5) == 2:
                    maze[y][x] = MAZE_MONEY

                if x == width - 2:
                    maze[y+1][x] = MAZE_EMPTY
                    continue
                if y == height - 2:
                    maze[y][x+1] = MAZE_EMPTY
                    continue

                if random.randint(0, 1) == 0:
                    maze[y][x+1] = MAZE_EMPTY
                else:
                    maze[y+1][x] = MAZE_EMPTY
            if x == 0 or y == 0:
                
                if not has_end and random.randint(0, 2) == 2 and isgoodendpoint(x, y, maze):
                   
                   has_end = True
                   maze[y][x] = MAZE_END
    maze[height - 1][width - 2] = MAZE_WALL
    centerx = math.ceil(width / 2)
    centery = math.ceil(height / 2)
    maze[centery][centerx] = MAZE_SHOP
                
            

    return maze


def isgoodendpoint(x, y, maze):
    if x == 0:
        if y == 0 or y == len(maze) - 1:
            return False
        if maze[y][x+1] == MAZE_EMPTY:
            return True
    if x == len(maze[0]) - 1:
        if y == len(maze) - 1 or y == 0:
            return False
        if maze[y][x-1] == MAZE_EMPTY:
            return True
    if y == 0 and maze[y+1][x] == MAZE_EMPTY:
       
        return True
    if y == len(maze) - 1 and maze[y-1][x] == MAZE_EMPTY:
        return True
    return False


def generate_wall_board(width, height):
    board = []
    for i in range(0, height):
        board.append([MAZE_WALL] * width)
    return board

def tostring(maze):
    returnstr = ""
    for row in maze:
        returnstr += "".join(row) + "-"
    return returnstr

def tolist(string : str):
    returnlist = []
    for row in string.split("-"):
        returnlist.append(list(row))
    return returnlist


if __name__ == '__main__':
    import pygame
    pygame.init()
    display = pygame.display.set_mode((550, 550))
    maze1 = generate_maze(11, 11)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        for y, row in enumerate(maze1):
            for x, cell in enumerate(row):
                pygame.draw.rect(display, (0, 0, 0) if cell == MAZE_WALL else (255, 255, 255), (x * 50, y * 50, 50, 50))
        pygame.display.update()

