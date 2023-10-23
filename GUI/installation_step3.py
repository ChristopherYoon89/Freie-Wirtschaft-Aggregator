from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
import os
import json
import configparser
import sys
from kivy.properties import ObjectProperty
from filechooser import FileChooser
import webbrowser



Builder.load_file("installation_step3screen.kv")


url = "https://www.google.at/search?q=Download+Google+Chrome"


class InstallationStepThreeScreen(MDScreen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		pass


	def download_google_chrome(self):
		webbrowser.open(url)