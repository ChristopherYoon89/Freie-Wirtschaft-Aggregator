
# pyinstaller --onefile --add-data "algorithms.py." --add-data "colors.py;." --add-data "configure.py;." --add-data "crawl_get_twitter_urls.py;." --add-data "crawler_main.py;." --add-data "crawler_twitter.py;." --add-data "data_manager.py;." --add-data "data_pipeline.py;." --add-data "datacrawler.py;." --add-data "datapipeline.py;." --add-data "filechooser.py;." --add-data "home.py;." --add-data "installation_home.py;." --add-data "installation_step1.py;." --add-data "installation_step2.py;." --add-data "installation_step3.py;." --add-data "installation_step4.py;." --add-data "installation_step5.py;." --add-data "installation.py;." --add-data "spinner.py;." pyinstaller --onefile --add-data "algorithms.py;." --add-data "colors.py;." --add-data "configure.py;." --add-data "crawl_get_twitter_urls.py;." --add-data "crawler_main.py;." --add-data "crawler_twitter.py;." --add-data "data_manager.py;." --add-data "data_pipeline.py;." --add-data "datacrawler.py;." --add-data "datapipeline.py;." --add-data "filechooser.py;." --add-data "home.py;." --add-data "installation_home.py;." --add-data "installation_step1.py;." --add-data "installation_step2.py;." --add-data "installation_step3.py;." --add-data "installation_step4.py;." --add-data "installation_step5.py;." --add-data "installation.py;." --add-data "spinner.py;." --add-data "configurescreen.kv;." --add-data "datacrawlerscreen.kv;." --add-data "datapipelinescreen.kv;." --add-data "filechooserscreen.kv;." --add-data "homescreen.kv;." --add-data "installation_homescreen.kv;." --add-data "installation_step1screen.kv;." --add-data "installation_step2screen.kv;." --add-data "installation_step3screen.kv;." --add-data "installation_step4screen.kv;." --add-data "installation_step5screen.kv;." --add-data "spinner.kv;." main.py

import kivy
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from home import HomeScreen
import kivymd.icon_definitions
from colors import colors


kivy.require('2.2.1')

Window.fullscreen = False


class MainApp(MDApp):
	'''
	Initializes the main app
	'''	

	title = 'Kraken-Technologies'
	
	def build(self):
		Window.maximize()
		
		
		# Initiate and define screen manager
		psm = ScreenManager()
		self.psm = psm
		
		ps1 = HomeScreen(name = "homescreen")
		psm.add_widget(ps1)

		psm.current = "homescreen"

		return psm


if __name__ == '__main__':
	MainApp().run()