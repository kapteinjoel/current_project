import math
from kivy.core.image import Image
from kivy.graphics.vertex_instructions import Rectangle
from kivy.metrics import dp

class World:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sky = Image('Assets/Images/sky.png').texture
        self.ground = Image('Assets/Images/ground.png').texture
        self.tile_count_y = 4
        self.tile_count_x = 4

    #draw the background tiles, they also dynamically adjust based on camera position x and y
    def render(self,camera_x, camera_y):
        for y in range(self.tile_count_y):
            for x in range(self.tile_count_x):
                tile_x = 960 + (self.tile_count_x * -500) + (x * 1000)
                tile_y = 1000 + (self.tile_count_y * -500) + (y * 1000)
                if y == 0:
                    Rectangle(texture=self.ground, pos=(tile_x - camera_x, tile_y - camera_y), size=(dp(1000), dp(1000)))
                else:
                    Rectangle(texture=self.sky, pos=(tile_x - camera_x, tile_y - camera_y), size=(dp(1000), dp(1000)))



