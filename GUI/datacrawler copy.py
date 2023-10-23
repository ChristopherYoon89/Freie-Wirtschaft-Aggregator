from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
import os
import json
import configparser
import sys
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.list import ThreeLineAvatarIconListItem, IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, ObjectProperty, ListProperty
import sys
import configparser
import multiprocessing
from kivy.clock import Clock
from data_manager import (
    get_json_filepath_crawling_sources, 
    get_config_filepath, 
    create_new_dataset, 
    get_latest_crawling_sources_data, 
    create_excel_template, 
    get_latest_crawling_sources_data_with_key,
    convert_excel_into_json
)
from crawler_main import crawling_process
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.factory import Factory
from filechooser import FileChooser
from kivymd.toast import toast 



MAX_MESSAGE_COUNT = 100


Builder.load_file("datacrawlerscreen.kv")

'''try:
	json_filepath_crawling_sources_data = get_json_filepath_crawling_sources()
	
	if json_filepath_crawling_sources_data == "":
		crawl_sources_data_list = None 
	else:
		with open(json_filepath_crawling_sources_data, "r", encoding="utf-8") as json_file:
			content = json_file.read()
			data = json.loads(content)

		crawl_sources_data_list = data['CrawlingSources']
except:
	crawl_sources_data_list = None'''



class QueueListItem(ThreeLineAvatarIconListItem):
	icon=StringProperty("")
	sources_data_list = None 	

	def move_down(self):
		self.crawl_sources_data_list = get_latest_crawling_sources_data()
		container = self.parent  # Get the parent GridLayout
		if self in container.children:
			item_index = container.children.index(self)
			if item_index > 0:
				# Swap the item with the one above it
				container.remove_widget(self)
				container.add_widget(self, item_index - 1)

				total_items = len(self.crawl_sources_data_list)
				correct_index = total_items - item_index - 1
				item_data = self.crawl_sources_data_list[correct_index]

				item_data = self.crawl_sources_data_list.pop(correct_index)
				self.crawl_sources_data_list.insert(correct_index + 1, item_data)

				self.save_crawl_sources_data()
				return True
		return False
					
				
	def move_up(self):
		self.crawl_sources_data_list = get_latest_crawling_sources_data()
		container = self.parent  # Get the parent GridLayout
		if self in container.children:
			item_index = container.children.index(self)
			if item_index > 0 or item_index == 0:
				# Swap the item with the one above it
				container.remove_widget(self)
				container.add_widget(self, item_index + 1)
				total_items = len(self.crawl_sources_data_list)
				correct_index = total_items - item_index - 1
				item_data = self.crawl_sources_data_list.pop(correct_index)
				self.crawl_sources_data_list.insert(correct_index - 1, item_data)
				print(self.crawl_sources_data_list)
				self.save_crawl_sources_data()
				return True
		return False


	def save_crawl_sources_data(self):
		# Assuming crawl_sources_data is a list of dictionaries
		json_filepath_crawling_sources_data = get_json_filepath_crawling_sources()
		with open(json_filepath_crawling_sources_data, "r", encoding="utf-8") as json_file:
			data = json.load(json_file)

		# Update the data with the new order
		data = {"CrawlingSources": self.crawl_sources_data_list}

		# Save the updated data back to the file
		with open(json_filepath_crawling_sources_data, "w", encoding="utf-8") as json_file:
			json.dump(data, json_file, indent=4)

	
	def delete_item(self):
		print("Delete item!")
		self.crawl_sources_data_list = get_latest_crawling_sources_data()
		container = self.parent  # Get the parent GridLayout
		if self in container.children:
			item_index = container.children.index(self)
			total_items = len(self.crawl_sources_data_list)
			correct_index = total_items - item_index - 1

			if correct_index >= 0:
				# Remove the item from the list widget
				container.remove_widget(self)

				# Remove the item from the JSON list
				deleted_item = self.crawl_sources_data_list.pop(correct_index)

				self.save_crawl_sources_data()
				self.show_toast("Entry was deleted!")
				return True
		return False
	

	def show_toast(self, text):
		'''
		Function to show message to user and reenter screen
		'''
		toast(text)


class RightContainer(IRightBodyTouch, MDBoxLayout):
	adaptive_width = True
	


class ContentShowDetails(BoxLayout):
	pass



class ContentAddSource(BoxLayout):
	pass



class ContentCreateSourceDataset(BoxLayout):
	pass



class ContentCreateExcelTemplate(BoxLayout):
	pass



class IconButtonTooltips(MDIconButton, MDTooltip):
	pass



class MDDialogCustomEditSource(MDDialog):
	def on_touch_down(self, touch):
		# Check if the touch is outside the dialog
		if not self.collide_point(*touch.pos):
			# Clear the text field
			if self.content_cls:
				# Dismiss the dialog
				self.dismiss()
		return super().on_touch_down(touch)
	


class MDDialogCustomAddSource(MDDialog):
	def on_touch_down(self, touch):
		# Check if the touch is outside the dialog
		if not self.collide_point(*touch.pos):
			# Clear the text field
			if self.content_cls:
				self.content_cls.ids.crawling_add_source_name_text.text = ""
				self.content_cls.ids.crawling_add_source_url_text.text = ""
				self.content_cls.ids.crawling_add_source_scrolls_text.text = ""
			# Dismiss the dialog
				self.dismiss()
			
		return super().on_touch_down(touch)
	

class MDDialogCustomCreateDataset(MDDialog):
	def on_touch_down(self, touch):
		# Check if the touch is outside the dialog
		if not self.collide_point(*touch.pos):
			# Clear the text field
			if self.content_cls:
				self.content_cls.ids.crawling_create_source_dataset_name_text.text = ""
				
				# Dismiss the dialog
				self.dismiss()
			
		return super().on_touch_down(touch)
	


class MDDialogCustomCreateExcelTemplate(MDDialog):
	def on_touch_down(self, touch):
		# Check if the touch is outside the dialog
		if not self.collide_point(*touch.pos):
			# Clear the text field
			if self.content_cls:
				self.content_cls.ids.crawling_create_excel_template_name_text.text = ""
				
				# Dismiss the dialog
				self.dismiss()
			
		return super().on_touch_down(touch)



class DataCrawlerScreen(MDScreen):
	dialog_edit_details = None
	dialog_add_source = None
	dialog_create_dataset = None
	dialog_create_excel_template = None
	crawl_sources_data_list = ListProperty([])

	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
		self.output_queue = multiprocessing.Queue()
		self.message_history = []


	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "Orange"
		self.dialog_edit_details = None
		self.dialog_add_source = None
		self.dialog_create_dataset = None
		self.dialog_create_excel_template = None
		self.file_chooser_opened = False
		self.crawl_sources_data_list = get_latest_crawling_sources_data()


	def on_enter(self):
		'''
		Method called when user enters screen 
		'''

		self.crawl_sources_data_list = get_latest_crawling_sources_data()

		# Add layout and spinner to screen 
		self.container_scroll_queue_list = self.ids.container_scroll_queue_list
		self.container_queue_list = self.ids.container_queue_list
		self.crawling_output_text = self.ids.crawling_output_text		
		self.container_scroll_queue_layout = self.ids.container_scroll_queue_layout

		self.container_queue_list.clear_widgets()

		# Check if queuedata includes any entries or is empty
		if self.crawl_sources_data_list == []:
			self.empty_queue_label = MDLabel(
				text = "No dataset selected",
				halign='center',
				valign='center',
				theme_text_color = "Custom",
				text_color = [1, 1, 1, 1]
			)
			self.container_scroll_queue_layout.add_widget(self.empty_queue_label)
		else:
			for item in self.crawl_sources_data_list:
				self.container_queue_list.add_widget(
					QueueListItem(
					text=f"{item['Name']}",
					secondary_text=f"{item['Url']}",
					tertiary_text=f"No. of scrolls: {item['No_of_scrolls']}",
					on_press=lambda x: self.show_source_detail_dialog(x, self.crawl_sources_data_list),
					icon="delete-outline",
					theme_text_color="Custom",
					text_color=[1, 1, 1, 1],
					secondary_theme_text_color="Custom",
					secondary_text_color=[152/255, 152/255, 152/255, 1],
					tertiary_theme_text_color="Custom",
					tertiary_text_color=[152/255, 152/255, 152/255, 1],
					divider_color=[132/255, 132/255, 132/255, 1],
					)
				)


	def callback_start_crawling_process(self):
		self.crawling_output_text.text = 'Start crawling process...'
		self.crawling_process = multiprocessing.Process(target=crawling_process, args=(self.output_queue,)) #, self.driver))
		self.crawling_process.start()
		Clock.schedule_interval(self.update_output_widget, 0.1)


	def update_output_widget(self, dt):
		if not self.output_queue.empty():
			message = self.output_queue.get()
			self.message_history.insert(0, message)
			self.message_history = self.message_history[:MAX_MESSAGE_COUNT]
			self.crawling_output_text.text = "".join(self.message_history)


	def show_source_detail_dialog(self, x, crawl_sources_data_list):
		app = MDApp.get_running_app()
		item_link = x.secondary_text
		item_name = "" 
		item_no_of_scrolls = ""
		for item in crawl_sources_data_list:
			if item_link == item['Url']:
				item_name = item["Name"]
				item_no_of_scrolls = item["No_of_scrolls"]

		if not self.dialog_edit_details:
			self.dialog_edit_details = MDDialogCustomEditSource(
				title= "[color=ffffff]Source Details[/color]",
				type="custom",
				md_bg_color=(0.1, 0.1, 0.1, 1),
				content_cls=ContentShowDetails(),
				buttons=[
					MDFlatButton(
						text="CANCEL",
						theme_text_color="Custom",
						text_color=app.theme_cls.primary_color,
						on_press=self.dismiss_details_and_edit_dialog,
					),
					MDFlatButton(
						text="SAVE",
						theme_text_color="Custom",
						text_color=app.theme_cls.primary_color,
						on_press=self.save_edited_entry,
					),
				],
			)

		content = self.dialog_edit_details.content_cls
		content.ids.crawling_sources_name_text.hint_text = item_name
		content.ids.crawling_sources_url_text.hint_text = item_link
		content.ids.crawling_sources_scroll_label.hint_text = str(item_no_of_scrolls)
		self.dialog_edit_details.open()


	def save_edited_entry(self, instance):
		if self.dialog_edit_details:
			self.dialog_edit_details.dismiss()

			content_edit_entry = self.dialog_edit_details.content_cls
			item_name = content_edit_entry.ids.crawling_sources_name_text.hint_text
			item_url = content_edit_entry.ids.crawling_sources_url_text.hint_text
			item_no_of_scrolls = content_edit_entry.ids.crawling_sources_scroll_label.hint_text

			print(item_name)
			print(item_url)
			print(item_no_of_scrolls)

			content_edit_entry = self.dialog_edit_details.content_cls
			edited_name = content_edit_entry.ids.crawling_sources_name_text.text
			print(edited_name)			

			edited_url = content_edit_entry.ids.crawling_sources_url_text.text
			print(edited_url)

			edited_no_of_scrolls = content_edit_entry.ids.crawling_sources_scroll_label.text
			print(edited_no_of_scrolls)

			crawl_sources_data_list = get_latest_crawling_sources_data_with_key()

			if edited_name != "" or edited_url != "" or edited_no_of_scrolls != "":
				for item in crawl_sources_data_list["CrawlingSources"]:
					if item['Name'] == item_name and item['Url'] == item_url and item['No_of_scrolls'] == item_no_of_scrolls:
						if not edited_name == "":
							item['Name'] = edited_name 
						if not edited_url == "":
							item['Url'] = edited_url 
						if not edited_no_of_scrolls == "":
							item['No_of_scrolls'] = edited_no_of_scrolls

					json_filepath_crawling_sources_data = get_json_filepath_crawling_sources()

					# Save the updated JSON data back to the file
					with open(json_filepath_crawling_sources_data, "w", encoding="utf-8") as json_file:
						json.dump(crawl_sources_data_list, json_file, indent=4, ensure_ascii=False)
					  # Exit the loop after updating the item
			
			
			content_edit_entry = self.dialog_edit_details.content_cls
			content_edit_entry.ids.crawling_sources_name_text.text = ""
			content_edit_entry.ids.crawling_sources_url_text.text = ""
			content_edit_entry.ids.crawling_sources_scroll_label.text = ""
			
			self.set_sources_list()
			self.show_toast("Save edited dataset")


	def dismiss_details_and_edit_dialog(self, instance):
		if self.dialog_edit_details:
			self.dialog_edit_details.dismiss()

			content_add_source = self.dialog_edit_details.content_cls
			content_add_source.ids.crawling_sources_name_text.text = ""
			content_add_source.ids.crawling_sources_url_text.text = ""
			content_add_source.ids.crawling_sources_scroll_label.text = ""
		


	def show_add_source_dialog(self):
		app = MDApp.get_running_app()

		if not self.dialog_add_source:
			self.dialog_add_source = MDDialogCustomAddSource(
				title= "[color=ffffff]Add Source[/color]",
				type="custom",
				md_bg_color=(0.1, 0.1, 0.1, 1),
				content_cls=ContentAddSource(),
				buttons=[
					MDFlatButton(
						text="CANCEL",
						theme_text_color="Custom",
						text_color=app.theme_cls.primary_color,
						on_press=self.dismiss_new_entry_dialog,
					),
					MDFlatButton(
						text="SAVE",
						theme_text_color="Custom",
						text_color=app.theme_cls.primary_color,
						on_press=self.save_new_entry,
					),
				],
			)

		self.dialog_add_source.open()


	def save_new_entry(self, instance):
		if self.dialog_add_source:
			content_add_source = self.dialog_add_source.content_cls
			name_text = content_add_source.ids.crawling_add_source_name_text.text
			url_text = content_add_source.ids.crawling_add_source_url_text.text
			scrolls_text = content_add_source.ids.crawling_add_source_scrolls_text.text
			
			# Now you can use name_text, url_text, and scrolls_text as needed
			print("Name:", name_text)
			print("URL:", url_text)
			print("Number of Scrolls:", scrolls_text)

			new_entry = {
				"Name": name_text, 
				"Url": url_text, 
				"No_of_scrolls": scrolls_text
			}
			
			json_filepath_crawling_sources_data = get_json_filepath_crawling_sources()

			with open(json_filepath_crawling_sources_data, "r", encoding="utf-8") as json_file:
				content = json_file.read()
				data = json.loads(content)

			data['CrawlingSources'].append(new_entry)

			with open(json_filepath_crawling_sources_data, "w", encoding="utf-8") as json_file:
				json.dump(data, json_file, indent=4)

			self.dialog_add_source.dismiss()

			content_add_source = self.dialog_add_source.content_cls
			content_add_source.ids.crawling_add_source_name_text.text = ""
			content_add_source.ids.crawling_add_source_url_text.text = ""
			content_add_source.ids.crawling_add_source_scrolls_text.text = ""

			self.set_sources_list()
			self.show_toast("New entry added!")


	def dismiss_new_entry_dialog(self, instance):
		if self.dialog_add_source:
			self.dialog_add_source.dismiss()

			content_add_source = self.dialog_add_source.content_cls
			content_add_source.ids.crawling_add_source_name_text.text = ""
			content_add_source.ids.crawling_add_source_url_text.text = ""
			content_add_source.ids.crawling_add_source_scrolls_text.text = ""
			

	def set_sources_list(self):

		'''json_filepath_crawling_sources_data = get_json_filepath_crawling_sources()

		with open(json_filepath_crawling_sources_data, "r", encoding="utf-8") as json_file:
			content = json_file.read()
			data = json.loads(content)

		crawl_sources_data_list = data['CrawlingSources']'''

		self.crawl_sources_data_list = get_latest_crawling_sources_data()

		self.container_queue_list = self.ids.container_queue_list
		self.container_queue_list.clear_widgets()
		
		if self.crawl_sources_data_list == []:
			self.empty_queue_label = MDLabel(
				text = "No dataset selected",
				halign='center',
				valign='center',
				theme_text_color = "Custom",
				text_color = [1, 1, 1, 1]
			)
			self.container_scroll_queue_layout.add_widget(self.empty_queue_label)
		else:
			self.container_queue_list.clear_widgets()
			for item in self.crawl_sources_data_list:
				self.container_queue_list.add_widget(
					QueueListItem(
					text=f"{item['Name']}",
					secondary_text=f"{item['Url']}",
					tertiary_text=f"No. of scrolls: {item['No_of_scrolls']}",
					on_press=lambda x: self.show_source_detail_dialog(x, self.crawl_sources_data_list),
					icon="delete-outline",
					theme_text_color="Custom",
					text_color=[1, 1, 1, 1],
					secondary_theme_text_color="Custom",
					secondary_text_color=[152/255, 152/255, 152/255, 1],
					tertiary_theme_text_color="Custom",
					tertiary_text_color=[152/255, 152/255, 152/255, 1],
					divider_color=[132/255, 132/255, 132/255, 1],
					)
				)


	def open_dataset_file_chooser(self):
		self.file_chooser = FileChooser(callback=self.save_dataset_path)
		self.file_chooser.show_load()
		self.file_chooser_opened = True


	def save_dataset_path(self):
		self.file_path = self.file_chooser.text_input.text
		config_path = get_config_filepath()
		filepath = self.file_chooser.selected_file_path
		print(filepath)
		print(config_path)
		
		if filepath:
			config = configparser.ConfigParser()
			config.read(config_path)
			config.set("Paths", "last_sources_dataset_filepath", filepath)
			
			with open(config_path, 'w') as configfile:
				config.write(configfile) 

		try:
			self.container_scroll_queue_layout.remove_widget(self.empty_queue_label)
		except:
			pass
		
		self.set_sources_list()

	
	def show_create_source_dataset_dialog(self):
		app = MDApp.get_running_app()

		if not self.dialog_create_dataset:
			self.dialog_create_dataset = MDDialogCustomCreateDataset(
				title= "[color=ffffff]Create Source Dataset[/color]",
				type="custom",
				md_bg_color=(0.1, 0.1, 0.1, 1),
				content_cls=ContentCreateSourceDataset(),
				buttons=[
					MDFlatButton(
						text="CANCEL",
						theme_text_color="Custom",
						text_color=app.theme_cls.primary_color,
						on_press=self.dismiss_create_source_dataset_dialog,
					),
					MDFlatButton(
						text="SAVE",
						theme_text_color="Custom",
						text_color=app.theme_cls.primary_color,
						on_press=self.save_create_source_dataset,
					),
				],
			)

		self.dialog_create_dataset.open()

	
	def dismiss_create_source_dataset_dialog(self, instance):
		if self.dialog_create_dataset:
			self.dialog_create_dataset.dismiss()

			content_add_source = self.dialog_create_dataset.content_cls
			content_add_source.ids.crawling_create_source_dataset_name_text.text = ""


	def save_create_source_dataset(self, instance):
		if self.dialog_create_dataset:
			self.dialog_create_dataset.dismiss()

			content_add_source = self.dialog_create_dataset.content_cls
			name_dataset = content_add_source.ids.crawling_create_source_dataset_name_text.text
			print(name_dataset)			

			content_add_source.ids.crawling_create_source_dataset_name_text.text = ""
			create_new_sources_dataset = create_new_dataset(name_dataset)
			self.show_toast("New dataset created")



	def show_create_excel_template_dialog(self):
		app = MDApp.get_running_app()

		if not self.dialog_create_excel_template:
			self.dialog_create_excel_template = MDDialogCustomCreateExcelTemplate(
				title= "[color=ffffff]Create Excel Template[/color]",
				type="custom",
				md_bg_color=(0.1, 0.1, 0.1, 1),
				content_cls=ContentCreateExcelTemplate(),
				buttons=[
					MDFlatButton(
						text="CANCEL",
						theme_text_color="Custom",
						text_color=app.theme_cls.primary_color,
						on_press=self.dismiss_create_excel_template_dialog,
					),
					MDFlatButton(
						text="SAVE",
						theme_text_color="Custom",
						text_color=app.theme_cls.primary_color,
						on_press=self.save_create_excel_template,
					),
				],
			)

		self.dialog_create_excel_template.open()


	def dismiss_create_excel_template_dialog(self, instance):
		if self.dialog_create_excel_template:
			self.dialog_create_excel_template.dismiss()

			content_add_source = self.dialog_create_excel_template.content_cls
			content_add_source.ids.crawling_create_excel_template_name_text.text = ""


	def save_create_excel_template(self, instance):
		if self.dialog_create_excel_template:
			self.dialog_create_excel_template.dismiss()

			content_add_source = self.dialog_create_excel_template.content_cls
			name_dataset = content_add_source.ids.crawling_create_excel_template_name_text.text
			print(name_dataset)			

			content_add_source.ids.crawling_create_excel_template_name_text.text = ""
			create_new_sources_dataset = create_excel_template(name_dataset)
			self.show_toast("New Excel template created")


	def convert_dataset_file_chooser(self):
		self.file_chooser_convert = FileChooser(callback=self.convert_dataset_path)
		self.file_chooser_convert.show_load()
		self.file_chooser_convert_opened = True


	def convert_dataset_path(self):
		self.file_path = self.file_chooser_convert.text_input.text
		
		filepath = self.file_chooser_convert.selected_file_path
		print(filepath)
		
		convert_dataset = convert_excel_into_json(filepath)


	def show_toast(self, text):
		'''
		Function to show message to user and reenter screen
		'''
		toast(text)
