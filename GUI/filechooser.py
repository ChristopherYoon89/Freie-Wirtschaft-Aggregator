from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
import os
from kivy.lang import Builder
import configparser


Builder.load_file("filechooserscreen.kv")

class LoadDialog(FloatLayout):
	load = ObjectProperty(None)
	cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
	save = ObjectProperty(None)
	text_input = ObjectProperty(None)
	cancel = ObjectProperty(None)


class FileChooser(FloatLayout):
	loadfile = ObjectProperty(None)
	savefile = ObjectProperty(None)
	text_input = ObjectProperty(None)
	selected_file_path = StringProperty("")

	def __init__(self, callback, **kwargs):
		super().__init__(**kwargs)

		self.callback = callback

	def dismiss_popup(self):
		self._popup.dismiss()

	def show_load(self):
		content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
		content.ids.filechooser.path = os.path.expanduser("~")
		content.ids.filechooser.dirselect = True
		self._popup = Popup(title="Select", content=content,
							size_hint=(0.4, 0.5))
		self._popup.open()

	def show_save(self):
		content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
		self._popup = Popup(title="Save file", content=content,
							size_hint=(0.9, 0.9))
		self._popup.open()

	def load(self, path, filename):
		path = str(path)
		filename = str(filename)
		path_string = filename.strip("[]")
		path_string = path_string.strip("\'")
		self.selected_file_path = path_string  # Store the selected path
		self.text_input.text = path_string # Display the selected folder's path
		print(path_string)
		self.callback()
		self.dismiss_popup()

	def save(self, filepath):
		with open(filepath, 'w') as stream:
			stream.write(self.text_input.text)
		self.dismiss_popup()
		

Factory.register('Root', cls=FileChooser)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)