import pygame, sys, os, math
pygame.init()
displaysize = (1280,720)
display = pygame.display.set_mode(displaysize)
dir_ = os.listdir("./images")
images = {}
basic_board = [["r", "n", "b", "q", "k", "b", "n", "r"],
               ["g"]*8,
               ["g"]*8,
               ["g"]*8,
               ["g"]*8,
               ["g"]*8,
               ["P"]*8,
               ["R", "N", "B", "Q", "K", "B", "N", "R"]]
for fn in dir_:
    images[fn] = pygame.image.load("Images/"+fn)
def getfont(size):
    return pygame.font.Font("DoHyeon-Regular.ttf", size)


def showtext(text, font, color,pos):
    fontimg = font.render(text, True, color)
    
    display.blit(fontimg, pos)
class Piece:
    def __init__(self, Type, x, y):
        self.Type = Type
        self.x = x
        self.y = y

    def draw(self):
        size = displaysize[1] / 8
        piecesurface = None
        if self.Type == "r":
            piecesurface = images["chess_rock.png"]
        if self.Type == "n":
            piecesurface = images["chess_night.png"]
        if self.Type == "b":
            piecesurface = images["chess_bishop.png"]
        if self.Type == "p":
            piecesurface = images["chess_pone.png"]
        if self.Type == "q":
            piecesurface = images["chess_queen.png"]
        if self.Type == "k":
            piecesurface = images["chess_king.png"]
        
        x_offset = (displaysize[0] / 2) - (displaysize[1] / 2)
        if piecesurface:
            piecesurface = pygame.transform.scale(piecesurface, (size, size))
            rectx = x_offset + (self.x * size)
            recty = (self.y * size)
            display.blit(piecesurface, (rectx, recty))
    def getmovepos(self, lists):
        poslist = []
        bx = self.x
        by = self.y
        x = 0
        y = 0
        if self.Type == "r":
            for x in range(8 - bx):
                xx = bx + x
                yy = by
                if lists[yy][xx] == "g":
                    poslist.append((xx, yy))
            xx = 0
            yy = 0
    
            for xxx in range(8 - bx):
                xx = bx - xxx
                yy = by
                if lists[yy][xx] == "g":
                    poslist.append((xx, yy))
            xx = 0
            yy = 0
    
            for x in range(8 - bx):
                yy = by + x
                xx = bx
                if yy > 8:
                    yy = 8
                if yy < 0:
                    yy = 0
                if xx > 8:
                    xx = 8
                if xx < 0:
                    xx = 0               
                if lists[yy][xx] == "g":
                    poslist.append((xx, yy))
            xx = 0
            yy = 0
            for y in range(8 - by):
                yy = by - y
                xx = bx
                if lists[yy][xx] == "g":
                    poslist.append((xx, yy))
            xx = 0
            yy = 0


                
                

        if self.Type == "n":
            try:
                xx = bx + 2
                yy = by + 1
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
                xx = bx + 2
                yy = by - 1
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
                xx = bx + 1
                yy = by + 2
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
                xx = bx + 1
                yy = by - 2
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
                xx = bx - 2
                yy = by - 1
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
                xx = bx - 2
                yy = by + 1
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
                xx = bx - 1
                yy = by - 2
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
                xx = bx - 1
                yy = by + 2
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
            except IndexError:
                return poslist
        if self.Type == "b":
            for x in range(8 - bx):
                xx = bx + x
                yy = by + x
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
            for x in range(8 - bx):
                xx = bx - x
                yy = by - x
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
            for x in range(8 - bx):
                yy = by + x
                xx = bx - x
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
            for y in range(8 - by):
                yy = by - y
                xx = bx - y
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
        if self.Type == "p":
            yy = by + 1
            if lists[yy][ bx]:
                poslist.append((x, yy))
        if self.Type == "q":
            piecesurface = images["chess_queen.png"]
            for x in range(8 - bx):
                xx = bx + x
                yy = by + x
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
            for x in range(8 - bx):
                xx = bx - x
                yy = by - x
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
            for x in range(8 - bx):
                yy = by + x
                xx = bx - x
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
            for y in range(8 - by):
                yy = by - y
                xx = bx - y
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
            for x in range(8 - bx):
                xx = bx + x
                yy = by
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
            for x in range(8 - bx):
                xx = bx - x
                yy = by
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
            for x in range(8 - bx):
                yy = by + y
                xx = bx
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
            for y in range(8 - by):
                yy = by - y
                xx = bx
                if lists[yy][xx] == "g":
                    poslist.append((x, yy))
        if self.Type == "k":
            xx = bx + 1
            yy = by
            if lists[yy][xx] == "g":
                poslist.append((x, yy))
            xx = bx - 1
            yy = by
            if lists[yy][xx] == "g":
                poslist.append((x, yy))
            xx = bx
            yy = by - 1
            if lists[yy][xx] == "g":
                poslist.append((x, yy))
            xx = bx
            yy = by + 1
            if lists[yy][xx] == "g":
                poslist.append((x, yy))
            xx = bx + 1
            yy = by + 1
            if lists[yy][xx] == "g":
                poslist.append((x, yy))
            xx = bx - 1
            yy = by - 1
            if lists[yy][xx] == "g":
                poslist.append((x, yy))
            xx = bx + 1
            yy = by - 1
            if lists[yy][xx] == "g":
                poslist.append((x, yy))
            xx = bx - 1
            yy = by + 1
            if lists[yy][xx] == "g":
                poslist.append((x, yy))
                

        return poslist
    def collide(self,event):
        x_offset = (displaysize[0] / 2) - (displaysize[1] / 2)
        size = displaysize[1] / 8
        xxxx = x_offset + (self.x * size)
        yyyy = self.y * size
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                print(xxxx, yyyy, self.y)
                if pos[0] > xxxx and pos[0] < xxxx + size:
                    print("X ok", pos[1])
                    if pos[1] > yyyy and pos[1] < yyyy + size:
                        print("clicked!")
                        return True
                    
                    else:
                        xxxx = 0
                        yyyy = 0
                        return
                else:
                    return 
    def move(self, x,  y):
        self. x += x
        self.y += y
class Board:
    def __init__(self):
        pass
    def drawgrid(self):
        size = displaysize[1] / 8
        x_offset = (displaysize[0] / 2) - (displaysize[1] / 2)
        color1 = (254, 226, 154)
        color2 = (181, 90, 0)
        color = color1
        for x in range(8):
            for y in range(8):
                rectx = x_offset + (x * size)
                recty = (y * size)
                pygame.draw.rect(display, color, (rectx, recty, size, size))
                if color == color1:
                    color = color2
                else:
                    color = color1
            if color == color1:
                color = color2
            else:
                color = color1
    
    def drawpiece(self, lists):
        x = 0
        y = 0
        for y_list in lists:
            for types in y_list:
                
                piece = Piece(types, x, y)
                piece.draw()
                
                if piece.collide(lists):
                    return piece
                peice = None
                x += 1
            x = 0
            y += 1
    



def rungame():
    display.fill((245,245,190))
    boardclass = Board()
    board = basic_board
    clickedpiece = None
    
    while True:
        boardclass.drawgrid()
        
        if not clickedpiece:
            clickedpiece = boardclass.drawpiece(board)
        if clickedpiece:
            
            poslist = clickedpiece.getmovepos(board)
            
            for event in pygame.event.get():
                
                lenpos = len(poslist)

                
                if event.type == pygame.KEYDOWN:
                    the_num = 0
                    if lenpos > 1:
                        if event.key == pygame.K_1:
                            the_num = 1
                            print("okok")
                    if lenpos > 2:
                        if event.key == pygame.K_2:
                            the_num = 2
                    if lenpos > 3:
                        if event.key == pygame.K_3:
                            the_num = 3
                    if lenpos > 4:
                        if event.key == pygame.K_4:
                            the_num = 4
                    if lenpos > 5:
                        if event.key == pygame.K_5:
                            the_num = 5
                    if lenpos > 6:
                        if event.key == pygame.K_6:
                            the_num = 6
                    if lenpos > 7:
                        if event.key == pygame.K_7:
                            the_num = 7
                    if lenpos > 8:
                        if event.key == pygame.K_8:
                            the_num = 8
                    if lenpos > 9:
                        if event.key == pygame.K_9:
                            the_num = 9
                    if the_num > 1:
                        
                        postuple = poslist[the_num - 1]
                        print(postuple, "postuple", the_num, the_num)
                        board[clickedpiece.x][clickedpiece.y] = "g"
                        board[postuple[1]][postuple[0]] = clickedpiece.Type
                        if the_num != 0:
                            clickedpiece = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
        boardclass.drawpiece(board)
        
        pygame.display.update()
def home_screen():
    Doing = True
    while Doing:
        showtext("Network Chess Game", getfont(60), (255,255,255), (380, 100))
        showtext("Press a Key To start", getfont(30), (255,255,255), (500, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                rungame()
                Doing = False
        pygame.display.update()
if __name__ == "__main__":
    rungame()