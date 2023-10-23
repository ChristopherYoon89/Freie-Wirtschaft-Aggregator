from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
import os
import json
import configparser
import sys
from kivy.properties import ObjectProperty
from subprocess import Popen, PIPE


from datapipeline import DataPipelineScreen
from datacrawler import DataCrawlerScreen
from configure import ConfigureScreen

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivy.uix.boxlayout import BoxLayout

from colors import colors


# main_folder = os.path.dirname(os.path.abspath(sys.argv[0]))

Builder.load_file("homescreen.kv")


teal_200 = colors["Teal"]["200"]
orange_200 = colors["Orange"]["200"]
light_status_bar = colors["Light"]["StatusBar"]


class Content(BoxLayout):
    pass



class HomeScreen(MDScreen):
	top_app_bar = ObjectProperty()
	dialog = None

	def __init__(self,**kwargs):
		super().__init__(**kwargs)

		# Reference widgets by id
		self.screen_content = self.ids.screen_content


	def on_enter(self):

		# Set up screen manager
		csm = ScreenManager()
		cs3 = ConfigureScreen(name = "configurescreen")
		cs4 = DataCrawlerScreen(name = "datacrawlerscreen")
		cs5 = DataPipelineScreen(name = "datapipelinescreen")
		csm.add_widget(cs3)
		csm.add_widget(cs4)
		csm.add_widget(cs5)

		csm.current = "configurescreen"
		self.csm = csm
		self.screen_content.add_widget(csm)

		#process = Popen(['python3', 'installation.py'], stdout=PIPE, stderr=PIPE)


	def nav_change_to_configure_screen(self, screen_instance):
		print('inside configure screen')
		self.nav_drawer.set_state("close")
		self.csm.current = screen_instance

	
	def nav_change_to_datacrawler_screen(self, screen_instance):
		print('inside datacrawler screen')
		self.csm.current = screen_instance


	def nav_change_to_datapipeline_screen(self, screen_instance):
		print("inside datapipeline screen")
		self.csm.current = screen_instance


