class Renderer:
    def __init__(self, display, mapdata):
        self.display = display
        self.mapdata = mapdata
        self.tilewidth = 32
    def render(self, x, y):
        size = self.display.get_size()
        xtilesize = size[0] / self.tilewidth
        ytilesize = size[1] / self.tilewidth
        xtile = x / self.tilewidth
        ytile = y / self.tilewidth

        showmapdata = self.mapdata[ytile - 1:ytile + ytilesize + 1][xtile - 1:xtile + xtilesize + 1]
        offsetx = -(x % self.tilewidth)
        offsety = -(y % self.tilewidth)

        for y, horizental in enumerate(showmapdata):
            for x, tile in enumerate(horizental):
                y *= self.tilewidth
                x *= self.tilewidth
                self.display.blit(tile, (x - offsetx, y - offsety))



            

        

