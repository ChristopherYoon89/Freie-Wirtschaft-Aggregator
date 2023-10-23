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



Builder.load_file("installation_step4screen.kv")



def _save(download_url, filepath):
	print("downloading", download_url, "...")
	response = requests.get(download_url)
	z = zipfile.ZipFile(io.BytesIO(response.content))
	z.extractall(filepath)
	print(f"saved the driver to {filepath}/")


def _download(pf: str):
	chromium_version = _get_chrome_version(pf)
	base_url = 'https://chromedriver.storage.googleapis.com/'
	config_file = configparser.ConfigParser()
	config_file.read('/home/chris-yoon/News Kraken Crawler/Configuration/config.ini')
	main_folder = config_file['Paths']['main_folder_path'] 

	filepath = main_folder

	if pf == "linux":
		download_url = base_url+f'{chromium_version}/chromedriver_linux64.zip'
		_save(download_url, filepath)
	elif pf == 'darwin':
		download_url = base_url+f'{chromium_version}/chromedriver_mac64.zip'
		_save(download_url, filepath)
	elif pf == 'windows':
		download_url = base_url+f'{chromium_version}/chromedriver_win32.zip'
		_save(download_url, filepath)


def _get_chromium_version(release_string: str):
	version_number = re.search('\d+\.+\d+\.+\d+', release_string).group()
	print("Browser Version:", version_number)
	chromium_version = requests.get(f'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version_number}').text
	print("Chromium Version:", chromium_version)
	return chromium_version


def _get_chrome_version(pf: str):
	if pf == 'linux':
		command = "google-chrome --version"
		release_string = subprocess.check_output(command.split(" ")).decode('utf-8')
		version_number = _get_chromium_version(release_string)
		return version_number
	elif pf == 'darwin':
		command = "grep -a1 CFBundleShortVersionString /Applications/Google\ Chrome.app/Contents/Info.plist | tail -1"
		release_string = subprocess.check_output(command, shell=True).decode('utf-8')
		version_number = _get_chromium_version(release_string)
		return version_number
	elif pf == 'windows':
		command = 'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		release_string = [line.decode('utf-8') for line in process.stdout][2]
		version_number = _get_chromium_version(release_string)
		return version_number	
	


class InstallationStepFourScreen(MDScreen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
	
		self.boxlayout_step4 = self.ids.boxlayout_step_four

		self.spinner_widget = SpinnerWidget()
		self.add_widget(self.spinner_widget)


	def callback_download_google_chrome_webdriver(self):
		self.remove_widget(self.boxlayout_step4)
		self.spinner_widget.ids.spinner.active = True
		threading.Thread(target=self.download_google_chrome_webdriver).start()

	def download_google_chrome_webdriver(self):

		pf = platform.system().lower()
		print("Operating System:", pf)
		try:
			_download(pf)
			Clock.schedule_once(lambda x: self.update_gui("Webdriver was successfully downloaded!"))
		except:
			Clock.schedule_once(lambda x: self.update_gui("Download of webdriver failed!"))


	def update_gui(self, text):
		self.spinner_widget.ids.spinner.active = False 
		self.add_widget(self.boxlayout_step4)
		Clock.schedule_once(lambda dt: self.show_toast(text))


	def show_toast(self, text):
		'''
		Function to show message to user and reenter screen
		'''
		toast(text)