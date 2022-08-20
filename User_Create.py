import ssl
import urllib

import certifi
import pymongo
from kivy.uix.screenmanager import ScreenManager, Screen
from pymongo import MongoClient


class User_Create(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ca = certifi.where()
        uri = 'mongodb+srv://dbaccess:2969@cluster0.tiuzhzq.mongodb.net/?retryWrites=true&w=majority'
        self.database = pymongo.MongoClient(uri, tlsCAFile=ca)

        self.db = self.database['Tank_Game']

        self.cluster = self.db['User_Names']


    def create(self):
        txt = self.ids.input.text
        post = {'_id': txt}
        try:
            self.cluster.insert_one(post)
            self.manager.current = 'Title'

            #for doc in self.cluster.find():
             #   print(doc)
              #  print(doc['_id'])



        except:
            print('User already exists')
