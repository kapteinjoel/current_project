import math
import random
import threading
import time
from kivy.clock import Clock
from kivy.core.image import Image
from kivy.graphics.vertex_instructions import Rectangle
from kivy.metrics import dp

#units spawn this health bar upon creation
class Health_Bar:
    def __init__(self, width = 0, height = 0, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self.current_bar = 1
        self.health_bar = Image('Assets/Images/health_bar__{}.Png'.format(self.current_bar)).texture

    def set_health_bar(self, current):
        self.health_bar = Image('Assets/Images/health_bar__{}.Png'.format(current)).texture

    def set_target(self, camera_x, camera_y, x, y):
        Rectangle(texture=self.health_bar, pos=(x - camera_x,(y + self.height + 20) - camera_y), size=(dp(64), dp(11)))

class Unit:
    def __init__(self, x = 0, y = 0, unit_type = None, speed = 1.5, attack_speed = [.75, 2], award = [25,45], max_health = 100, height = 64, width = 64, damage = [10,20], targeting_distance = 80, direction = 'right', **kwargs):
        super().__init__(**kwargs)
        self.height = height
        self.width = width
        self.speed = speed
        self.attack_speed = attack_speed
        self.damage = damage
        self.direction = direction
        self.targeting_distance = targeting_distance
        self.health = max_health
        self.max_health = max_health
        self.award = award
        self.x = x
        self.y = y
        self.unit_type = unit_type
        self.able_to_attack = True
        self.set_animation()
        self.health_bar = Health_Bar(height = self.height)

    #dependent on unit_type
    def set_animation(self):
        if self.unit_type == None:
            self.unit_type = Image('Assets/Images/Tile.Png').texture

    #returns bots stats based on passed parameter
    #target is a unit you want the distance from
    def get_info(self, info, target = None):
        if info == 'x':
            return self.x
        if info == 'targeting_distance':
            return self.targeting_distance
        if info == 'distance':
            return abs(self.x - target)
        if info == 'health':
            return self.health
        if info == 'damage':
            return self.damage
        if info == 'award':
            return random.randint(self.award[0], self.award[1])

    #allows the changing of unit related stats
    def set_info(self, info, modifier):
        if info == 'health':
            self.health = self.health + modifier

    def move(self):
        if self.direction == 'right':
            self.x = self.x + self.speed
        else:
            self.x = self.x - self.speed

    def reset_attack(self, dt):
        self.able_to_attack = True

    def attack(self):
        if self.able_to_attack == True:
            self.able_to_attack = False
            Clock.schedule_once(self.reset_attack, random.uniform(self.attack_speed[0], self.attack_speed[1]))
            return random.randint(self.damage[0], self.damage[1])
        else:
            return 0

    def update(self, camera_x, camera_y):
        Rectangle(texture=self.unit_type, pos=(self.x - camera_x, self.y - camera_y), size=(dp(self.width), dp(self.height)))
        self.health_bar.set_target(camera_x, camera_y, self.x, self.y)
        try:
            #update current health bar based on health: health/maxhealth * number of health bar images
            self.health_bar.set_health_bar(math.ceil((self.health/self.max_health)*62))
        except:
            #lazy coding safety net :D, function above tends to fail
            pass