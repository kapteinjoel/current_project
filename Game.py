import threading
import time
import urllib

import certifi
import pymongo
from kivy.core.image import Image
from kivy.core.window import Window
from pymongo import MongoClient
from kivy.graphics.texture import Texture
from kivy.graphics.vertex_instructions import Rectangle
from kivy.metrics import dp
from kivy.properties import Clock
from kivy.uix.screenmanager import Screen

import Player, World, Unit

class Game(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #game loop variable
        self.loop = None

        #boolean that manages unit creation
        self.player_can_create = True
        self.bot_can_create = True

        #initialize classes <module.class>
        self.Player = Player.Player()
        self.Bot = Player.Bot()
        self.Camera = Player.Camera()
        self.World = World.World()

        #unit lists
        self.player_units = []
        self.bot_units = []

        #setup keyboard listener variables
        self.pressed_keys = set()
        self._keyboard = None

    def on_enter(self):
        #initiate keyboard
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        #start game loop clock using game loop variable
        self.loop = Clock.schedule_interval(self.game_loop, 1 / 60)

    def on_leave(self):
        #ends the game loop variable
        self.loop.cancel()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, *args):
        self.pressed_keys.add(keycode[1])
        return True

    def _on_keyboard_up(self, keyboard, keycode, *args):
        self.pressed_keys.remove(keycode[1])
        return True

    def process_keys(self):
        if 'w' in self.pressed_keys:
            self.Camera.move('w')
        if 's' in self.pressed_keys:
            self.Camera.move('s')
        if 'd' in self.pressed_keys:
            self.Camera.move('d')
        if 'a' in self.pressed_keys:
            self.Camera.move('a')
        if 'c' in self.pressed_keys:
            if self.player_can_create == True:
                self.player_units.append(Unit.Unit(x = -900))
                #units cant be created for designated amount of time in seconds
                self.player_can_create = False
                creation_timeout = Clock.schedule_once(self.unit_create_player, 1)
        if 'v' in self.pressed_keys:
            if self.bot_can_create == True:
                self.bot_units.append(Unit.Unit(x = 2750, direction = 'left'))
                #units cant be created for designated amount of time in seconds
                self.bot_can_create = False
                creation_timeout = Clock.schedule_once(self.unit_create_bot, 1)

    def unit_create_player(self, dt):
        self.player_can_create = True

    def unit_create_bot(self, dt):
        self.bot_can_create = True

    def game_loop(self, dt):
        #key presses
        self.process_keys()
        #update camera
        self.Camera.update()
        #clear canvas and then draw to it
        self.canvas.clear()
        with self.canvas:
            #draw world respective to camera
            self.World.render(self.Camera.get_X(), self.Camera.get_Y())

            # ==========================================================================
            # update PLAYER units
            # ==========================================================================
            for unit in self.player_units:
                #process stop points
                try:
                    unit_in_front_index = self.player_units.index(unit)-1
                    if unit_in_front_index == -1:
                        #set index to none to purposely break first try statement as -1 refers to last list element
                        unit_in_front_index = None
                    #stops based on friendly units (unit index -1) distance in front of currently referenced unit
                    if unit.get_info('distance', self.player_units[unit_in_front_index].get_info('x')) < 80:
                        pass
                    else:
                        try:
                            if unit.get_info('distance', self.bot_units[0].get_info('x')) < unit.get_info('targeting_distance'):
                                pass
                            else:
                                unit.move()
                        except:
                            unit.move()
                except:
                    try:
                        if unit.get_info('distance', self.bot_units[0].get_info('x')) < unit.get_info('targeting_distance'):
                            #PLAYER melee attacking
                            self.bot_units[0].set_info('health', -unit.attack())
                        else:
                            unit.move()
                    except:
                        unit.move()
                unit.update(self.Camera.get_X(), self.Camera.get_Y())
                if unit.get_info('x') > 2750:
                    self.player_units.remove(unit)
                if unit.get_info('health') < 1:
                    self.Bot.set_info('money', unit.get_info('award'))
                    self.player_units.remove(unit)

            #==========================================================================
            #update BOT units
            #==========================================================================
            for unit in self.bot_units:
                try:
                    unit_in_front_index = self.bot_units.index(unit) - 1
                    if unit_in_front_index == -1:
                        unit_in_front_index = None
                    if unit.get_info('distance', self.bot_units[unit_in_front_index].get_info('x')) < 80:
                        pass
                    else:
                        try:
                            if unit.get_info('distance', self.player_units[0].get_info('x')) < unit.get_info('targeting_distance'):
                                pass
                            else:
                                unit.move()
                        except:
                            unit.move()
                except:
                    try:
                        if unit.get_info('distance', self.player_units[0].get_info('x')) < unit.get_info('targeting_distance'):
                            #BOT melee attacking
                            self.player_units[0].set_info('health', -unit.attack())
                            pass
                        else:
                            unit.move()
                    except:
                        unit.move()

                unit.update(self.Camera.get_X(), self.Camera.get_Y())
                if unit.get_info('x') < -1000:
                    self.bot_units.remove(unit)
                if unit.get_info('health') < 1:
                    self.Player.set_info('money', unit.get_info('award'))
                    self.bot_units.remove(unit)