import os
import sys
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
import sys
from selenium.webdriver.support import expected_conditions as EC
import time
import configparser
from datetime import datetime
import json


def get_config_filepath():
	main_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
	folder_config_file = "Configuration"
	config_filename = "config.ini"
	config_filepath = os.path.join(main_folder, folder_config_file, config_filename)
	return config_filepath



def get_json_filepath_crawling_sources():
	config_path = get_config_filepath()
	print(config_path)
	if config_path:
		config = configparser.ConfigParser()
		config.read(config_path)
		json_filepath_crawling_sources_data = config['Paths']['last_sources_dataset_filepath']
	return json_filepath_crawling_sources_data



def get_name_of_latest_sources_dataset():
	json_filepath = get_json_filepath_crawling_sources()
	json_filename = os.path.splitext(os.path.basename(json_filepath))[0]
	if len(json_filename) > 10:
		json_filename = json_filename[:17] + "..."
	return json_filename



def get_latest_crawling_sources_data():
	json_filepath_crawling_sources_data = get_json_filepath_crawling_sources()
	
	if json_filepath_crawling_sources_data == "":
		crawl_sources_data_list = [] 
	else:
		try:
			with open(json_filepath_crawling_sources_data, "r", encoding="utf-8") as json_file:
				content = json_file.read()
				data = json.loads(content)
				crawl_sources_data_list = data['CrawlingSources']
		except: 
			crawl_sources_data_list = [] 
		
	return crawl_sources_data_list



def get_latest_crawling_sources_data_with_key():
	json_filepath_crawling_sources_data = get_json_filepath_crawling_sources()
	
	if json_filepath_crawling_sources_data == "":
		data = None 
	else:
		with open(json_filepath_crawling_sources_data, "r", encoding="utf-8") as json_file:
			content = json_file.read()
			data = json.loads(content)
	return data



def get_crawling_sources():
	json_filepath_crawling_sources_data = get_json_filepath_crawling_sources()
	
	# Load the JSON content
	with open(json_filepath_crawling_sources_data, "r", encoding="utf-8") as json_file:
		content = json.load(json_file)
	
	# Convert "CrawlingSources" to a pandas DataFrame
	df = pd.DataFrame(content['CrawlingSources'])
	df['Url'] = df['Url'].astype(str)
	df['No_of_scrolls'] = df['No_of_scrolls'].astype(int)
	return df



def create_new_dataset(filename):
	main_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
	links_and_sources_folder = "Links-and-Sources"
	new_dataset_filename = f"{filename}.json"
	new_dataset_filepath = os.path.join(main_folder, links_and_sources_folder, new_dataset_filename)

	data = {
			"CrawlingSources": [
				{
				"Name": "NA", 
				"Url": "NA",
				"No_of_scrolls": "NA",
				}
			]
		}

	with open(new_dataset_filepath, "w", encoding="utf-8") as json_file:
		json.dump(data, json_file, indent=4, ensure_ascii=False)
	


def json_dict_to_excel(json_dict):
	main_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
	folder_crawl_sources = "Links-and-Sources"
	json_filename_crawl_sources = "Links_daily_sources3.xlsx"
	xlsx_filepath_crawling_sources_data = str(os.path.join(main_folder, folder_crawl_sources, json_filename_crawl_sources)) 
	# Extract the list of dictionaries from the JSON dictionary
	data_list = json_dict["CrawlingSources"]

	# Create a DataFrame from the list of dictionaries
	df = pd.DataFrame(data_list)

	# Write the DataFrame to an Excel file
	df.to_excel(xlsx_filepath_crawling_sources_data, index=False)



def create_excel_template(templatename):
	main_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
	sources_and_links_folder = "Links-and-Sources"
	excel_filename = f"{templatename}.xlsx"
	excel_filepath = os.path.join(main_folder, sources_and_links_folder, excel_filename)

	list_name = ['NA']
	list_link = ['NA']
	list_no_of_scrolls = ['NA']

	df_list_name = pd.DataFrame(list_name)
	df_list_name.columns = ['Name']
	df_list_link = pd.DataFrame(list_link)
	df_list_link.columns = ['Url']
	df_list_no_of_scrolls = pd.DataFrame(list_no_of_scrolls)
	df_list_no_of_scrolls.columns = ['No_of_scrolls']

	df_excel_template = pd.concat([df_list_name, df_list_link, df_list_no_of_scrolls], axis=1)
	df_excel_template.to_excel(excel_filepath, header=True, index=None)


def convert_excel_into_json(filepath):

	excel_data = pd.read_excel(filepath)
	data = excel_data.to_dict(orient='records')

	json_data = {"CrawlingSources": data}
	print(json_data)

	data_with_headers = excel_data.to_dict(orient='records')
	json_data_with_headers = {"CrawlingSources": data_with_headers}

	filename = os.path.basename(filepath)
	filename_without_extension = os.path.splitext(filename)[0]
	json_filename = f"{filename_without_extension}.json"
	
	main_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
	links_and_sources_folder = "Links-and-Sources"
	json_filepath = os.path.join(main_folder, links_and_sources_folder, json_filename)

	# Save the JSON data to a file
	with open(json_filepath, 'w', encoding="utf-8") as json_file:
		json.dump(json_data_with_headers, json_file, indent=4, ensure_ascii=False)



def crawler_temporary_storage(status_link, text, external_link):
	main_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
	data_crawling_folder = "Data-Crawling"
	data_crawling_temp_storage_folder = "Storage-Temporary"
	data_crawling_temp_storage_path = os.path.join(main_folder, data_crawling_folder, data_crawling_temp_storage_folder)

	df_status_urls = pd.DataFrame(status_link)
	df_status_urls.columns = ['URL']
	df_status_texte = pd.DataFrame(text)
	df_status_texte.columns = ['TEXT']
	df_external_urls = pd.DataFrame(external_link)
	df_external_urls.columns = ['EXTERNAL_URL']
	df = pd.concat([df_status_urls, df_status_texte, df_external_urls], axis=1)

	date = pd.Timestamp.today().strftime('%Y-%m-%d')
	current_time = pd.Timestamp.now().strftime('%H-%M-%S')
	file_name_temporary = 'CRAWL_TEMPORARY_STORAGE-' + date + '-' + current_time + '.xlsx'
	temporary_file_path = os.path.join(data_crawling_temp_storage_path, file_name_temporary)

	try:
		df.to_excel(temporary_file_path, header=True, index=None)
		print("\n File saved successfully. \n")
	except Exception as e:
		print("\n Error occurred while saving the file: \n", str(e))



def crawler_final_storage(mydata_profile_final, mydata_texte_final, mydata_urls_final):
	'''
	Function that saves the crawling data into final storage
	'''
	main_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
	data_crawling_folder = "Data-Crawling"
	data_crawling_final_storage_folder = "Storage-Final"
	date = pd.Timestamp.today().strftime('%Y-%m-%d')
	current_time = pd.Timestamp.now().strftime('%H-%M-%S')
	file_name_final = 'DATASET_FINAL_RAW_' + date + '_' + current_time + '.xlsx'
	print("\nName of temporary file: \n", file_name_final)
	final_file_path = os.path.join(main_folder, data_crawling_folder, data_crawling_final_storage_folder, file_name_final)
	print("\nPath of final file: \n", final_file_path)

	df_status_urls = pd.DataFrame(mydata_profile_final)
	df_status_urls.columns = ['URL']
	df_status_texte = pd.DataFrame(mydata_texte_final)
	df_status_texte.columns = ['TEXT']
	df_external_urls = pd.DataFrame(mydata_urls_final)
	df_external_urls.columns = ['EXTERNAL_URL']

	df = pd.concat([df_status_urls, df_status_texte, df_external_urls], axis=1)
	print(df)
	df.to_excel(final_file_path, header=True, index=None)
		

		

