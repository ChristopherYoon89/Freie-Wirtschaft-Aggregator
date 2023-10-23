from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
import os
import json
import configparser
import sys
from kivy.properties import ObjectProperty



Builder.load_file("installation_step1screen.kv")



class InstallationStepOneScreen(MDScreen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		pass