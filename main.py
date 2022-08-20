import kivy
from kivy.core.window import Window
import wx

import Title, Game
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

kivy.require('1.9.0')

class DisplayManager(ScreenManager):
    pass

class Game(App):

    def build(self):
        app = wx.App(False)
        width, height = wx.GetDisplaySize()
        Window.size = (width, height)
        Window.fullscreen = True
        return Builder.load_file('display.kv')

if __name__ == '__main__':
    Game().run()