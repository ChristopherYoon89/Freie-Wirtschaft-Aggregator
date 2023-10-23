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
from spinner import SpinnerWidget
import time
import platform
import os
import subprocess
import requests
import zipfile
import io
import re
import threading
from kivymd.toast import toast 
from kivy.clock import Clock
import configparser



Builder.load_file("installation_step5screen.kv")

urls = [
    "https://raw.githubusercontent.com/ChristopherYoon89/Python/main/Links_daily_sources.csv",
]

main_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
links_and_sources_directory = "Links-and-Sources"
links_and_sources_file_name = "Links_daily_sources.csv"
links_and_sources_file_path = os.path.join(main_folder, links_and_sources_directory, links_and_sources_file_name)


def download_data_from_github(url, links_and_sources_path):

	response = requests.get(url)
	if response.status_code == 200:
		with open(links_and_sources_path, "wb") as file:
			file.write(response.content)
		print("File downloaded successfully.")
	else:
		print("Failed to download the file.")


class InstallationStepFiveScreen(MDScreen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
	
		self.boxlayout_step5 = self.ids.boxlayout_step_five

		self.spinner_widget = SpinnerWidget()
		self.add_widget(self.spinner_widget)
		self.links_and_sources_file_path = links_and_sources_file_path


	def callback_download_algorithms(self):
		self.remove_widget(self.boxlayout_step5)
		self.spinner_widget.ids.spinner.active = True
		threading.Thread(target=self.download_algorithms, args=(links_and_sources_file_path,)).start()


	def download_algorithms(self, links_and_sources_file_path):
		print("Download starts")
		try:
			for url in urls:
				download_data = download_data_from_github(url, links_and_sources_file_path)
			Clock.schedule_once(lambda dt: self.update_gui("Download of files was successful!"))
		except:
			Clock.schedule_once(lambda dt: self.update_gui("Download of files failed!"))


	def update_gui(self, text):
		self.spinner_widget.ids.spinner.active = False 
		self.add_widget(self.boxlayout_step5)
		Clock.schedule_once(lambda dt: self.show_toast(text))


	def show_toast(self, text):
		'''
		Function to show message to user and reenter screen
		'''
		toast(text)