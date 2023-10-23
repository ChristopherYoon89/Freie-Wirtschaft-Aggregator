import kivy
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from datetime import datetime
from kivy.core.window import Window
from kivy.config import Config
from colors import colors
from installation_home import InstallationHomeScreen


kivy.require('2.2.1')



class InstallationApp(MDApp):
	'''
	Initializes the installation app
	'''	

	title = 'Installation'
	
	def build(self):		

		self.theme_cls.colors = colors
		self.theme_cls.primary_palette = "Teal"
		self.theme_cls.accent_palette = "Orange"
		# Initiate and define screen manager
		ipsm = ScreenManager()
		self.ipsm = ipsm
		
		ipsm1 = InstallationHomeScreen(name = "installationhomescreen")
		ipsm.add_widget(ipsm1)
		ipsm.current = "installationhomescreen"
		return ipsm


if __name__ == '__main__':
	InstallationApp().run()