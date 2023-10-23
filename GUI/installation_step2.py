from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
import os
import io
import sys
import json
import configparser
import sys
from kivy.properties import ObjectProperty
from filechooser import FileChooser
from kivy.clock import Clock
from kivymd.toast import toast 
import configparser



Builder.load_file("installation_step2screen.kv")


def create_config_file(main_folder):
	# Create a new ConfigParser instance
	config = configparser.ConfigParser()

	# Add sections and parameters to the config
	config.add_section('Paths')
	config.set('Paths', 'main_folder_path', main_folder)
	config.set('Paths', 'last_sources_dataset_filepath', '')

	config_folder = "Configuration"
	config_file_name = "config.ini"
	config_folder_path = os.path.join(main_folder, config_folder)
	config_file_path = os.path.join(main_folder, config_folder_path, config_file_name)

	if not os.path.exists(config_folder_path):
		os.mkdir(config_folder_path)

	if not os.path.exists(config_file_path):
		# Write the config to a file
		with open(config_file_path, 'w') as configfile:
			config.write(configfile)
	


def create_folders(main_folder):
	main_folder = main_folder
	data_crawling_folder = "Data-Crawling"
	data_pipeline_folder = "Data-Pipeline"
	temp_storage = "Storage-Temporary"
	final_storage = "Storage-Final"
	dataset_raw = "Dataset-Raw"
	dataset_final = "Dataset-Final"
	links_and_sources_folder = "Links-and-Sources"
	algorithms_folder = "Algorithms"
	

	data_crawling_folder_path = os.path.join(main_folder, data_crawling_folder)
	data_pipeline_folder_path = os.path.join(main_folder, data_pipeline_folder)
	data_crawling_temp_storage_path = os.path.join(main_folder, data_crawling_folder, temp_storage)
	data_crawling_final_storage_path = os.path.join(main_folder, data_crawling_folder, final_storage)
	data_pipeline_temp_storage_path = os.path.join(main_folder, data_pipeline_folder, dataset_raw)
	data_pipeline_final_storage_path = os.path.join(main_folder, data_pipeline_folder, dataset_final)
	links_and_sources_folder_path = os.path.join(main_folder, links_and_sources_folder)
	algorithms_folder_path = os.path.join(main_folder, algorithms_folder)

	if not os.path.exists(data_crawling_folder_path):
		os.mkdir(data_crawling_folder_path)

	if not os.path.exists(data_pipeline_folder_path):
		os.mkdir(data_pipeline_folder_path)

	if not os.path.exists(data_crawling_temp_storage_path):
		os.mkdir(data_crawling_temp_storage_path)

	if not os.path.exists(data_crawling_final_storage_path):
		os.mkdir(data_crawling_final_storage_path)

	if not os.path.exists(data_pipeline_temp_storage_path):
		os.mkdir(data_pipeline_temp_storage_path)

	if not os.path.exists(data_pipeline_final_storage_path):
		os.mkdir(data_pipeline_final_storage_path)

	if not os.path.exists(links_and_sources_folder_path):
		os.mkdir(links_and_sources_folder_path)

	if not os.path.exists(algorithms_folder_path):
		os.mkdir(algorithms_folder_path)

	config_file = create_config_file(main_folder)



class InstallationStepTwoScreen(MDScreen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
		self.file_chooser_opened = False
		self.step2_next_buttion = self.ids.step2_next_buttion
		self.step2_next_buttion.disabled = True


	def open_file_chooser(self):
		self.file_chooser = FileChooser(callback=self.enable_next_button())
		self.file_chooser.show_load()
		self.file_chooser_opened = True

	
	def enable_next_button(self):
		if self.step2_next_buttion:
			self.step2_next_buttion.disabled = False


	def save_folder(self):
		self.file_path = self.file_chooser.text_input.text
		if self.file_chooser_opened:
			if self.file_chooser.text_input.text == "":
				Clock.schedule_once(lambda dt: self.show_toast("Select a valid folder"))
			else:
				create_folder = create_folders(self.file_chooser.text_input.text)
				app = MDApp.get_running_app()
				app.ipsm.get_screen("installationhomescreen").nav_change_to_step3_screen("installation_step_three_screen")

			print(self.file_chooser.text_input.text)
		else:
			Clock.schedule_once(lambda dt: self.show_toast("Select a valid folder"))
			print("Choose directory")


	def show_toast(self, text):
		'''
		Function to show message to user and reenter screen
		'''
		toast(text)