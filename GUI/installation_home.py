from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
import os
import json
import configparser
import sys
from kivy.properties import ObjectProperty

from installation_step1 import InstallationStepOneScreen
from installation_step2 import InstallationStepTwoScreen
from installation_step3 import InstallationStepThreeScreen
from installation_step4 import InstallationStepFourScreen
from installation_step5 import InstallationStepFiveScreen

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivy.uix.boxlayout import BoxLayout

from colors import colors

Builder.load_file("installation_homescreen.kv")


teal_200 = colors["Teal"]["200"]
orange_200 = colors["Orange"]["200"]
light_status_bar = colors["Light"]["StatusBar"]



class InstallationHomeScreen(MDScreen):
	top_app_bar = ObjectProperty()
	dialog = None

	def __init__(self,**kwargs):
		super().__init__(**kwargs)

		# Reference widgets by id
		self.screen_content = self.ids.screen_content


	def on_enter(self):

		# Set up screen manager
		icsm = ScreenManager()
		ics1 = InstallationStepOneScreen(name = "installation_step_one_screen")
		ics2 = InstallationStepTwoScreen(name = "installation_step_two_screen")
		ics3 = InstallationStepThreeScreen(name = "installation_step_three_screen")
		ics4 = InstallationStepFourScreen(name = "installation_step_four_screen")
		ics5 = InstallationStepFiveScreen(name = "installation_step_five_screen")
		icsm.add_widget(ics1)
		icsm.add_widget(ics2)
		icsm.add_widget(ics3)
		icsm.add_widget(ics4)
		icsm.add_widget(ics5)

		icsm.current = "installation_step_one_screen"
		self.icsm = icsm
		self.screen_content.add_widget(icsm)


	def nav_change_to_step1_screen(self, screen_instance):
		print('inside step1 screen')
		self.icsm.current = screen_instance

	
	def nav_change_to_step2_screen(self, screen_instance):
		print('inside step2 screen')
		self.icsm.current = screen_instance


	def nav_change_to_step3_screen(self, screen_instance):
		print('inside step3 screen')
		self.icsm.current = screen_instance

	
	def nav_change_to_step4_screen(self, screen_instance):
		print('inside step4 screen')
		self.icsm.current = screen_instance


	def nav_change_to_step5_screen(self, screen_instance):
		print('inside step5 screen')
		self.icsm.current = screen_instance


	def logout_action(self, *args):
		'''
		Function called when user logs out and resetting config file
		'''

		MDApp.get_running_app().stop()

