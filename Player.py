from kivy.core.image import Image
from kivy.graphics import texture
from kivy.graphics.vertex_instructions import Rectangle
from kivy.metrics import dp
from kivy.uix.widget import Widget

#manages viewport related actions
class Camera:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.x = 0
        self.y = 0
        self.speed = 10
        self.skin = Image('Assets/Images/Player.Png').texture

    def bind(self, x, y):
        self.x = x+32
        self.y = y+32
        print(self.x, self.y)

    def move(self, key):
        if key == 'w':
            self.y += self.speed
        if key == 's':
            self.y -= self.speed
        if key == 'd':
            self.x += self.speed
        if key == 'a':
            self.x -= self.speed

    def get_X(self):
        return int(self.x)
    def get_Y(self):
        return int(self.y)

    def update(self):
        #camera bounds
        if self.y < -220:
            self.y = -220
        if self.y > 1920:
            self.y = 1920
        if self.x < -1020:
            self.x = -1020
        if self.x > 1020:
            self.x = 1020

#manages player related variables and actions
class Player:
    def __init__(self, money = 500, xp = 0, **kwargs):
        super().__init__(**kwargs)
        self.money = money
        self.xp = xp

    def set_info(self, info, modifier):
        if info == 'money':
            self.money = self.money + modifier
            print('Player Money: ', self.money)

#manages bot related variables and actions
class Bot:
    def __init__(self, money = 500, xp = 0, **kwargs):
        super().__init__(**kwargs)
        self.money = money
        self.xp = xp

    def set_info(self, info, modifier):
        if info == 'money':
            self.money = self.money + modifier
            print('Bot Money: ', self.money)

    def decide_action(self):
        pass
