from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
import os
import json
import configparser
import sys
from kivy.properties import ObjectProperty



class ConfigureScreen(MDScreen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		pass



	def create_empty_json_file(self, json_filepath_mobimeddata):
		'''
		Function to create empty json file
		'''
		data = {
			"patientdata": [
				{
				"ID": "NA", 
				"Patient": "NA",
				"Age": "NA",
				}
			],
			"queuedata": [
				{
				"ID": "NA",
				"Patient": "NA",
				"File": "NA",
				"File_compressed": "NA",
				"Path": "NA",
				"Filetype": "NA",
				"Date": "NA",
				"Duration": "NA",
				}
			]
		}

		with open(json_filepath_mobimeddata, "w", encoding="utf-8-sig") as json_file:
			json.dump(data, json_file, indent=4, ensure_ascii=False)