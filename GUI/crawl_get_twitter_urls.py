# cd C:\Users\User\Documents\Python_Developing\Python\Freie-Wirtschaft-Crawler
# cd C:\Users\User\Documents\Python_Developing\Python\Freie-Wirtschaft-Crawler\dist
# Go to project folder and create virtual environment: python -m venv virtualenv fwenvironment
# fwenvironment\Scripts\activate

# pyinstaller --onefile --add-data "data/*;data/" my_script.py

# pyinstaller --onefile --add-data "configure_bot.py;." --add-data "crawl_daily_source.py;." --add-data "menu_configuration.py;." --add-data "menu_crawling.py;." --add-data "menu_help.py;." --add-data "menu_update.py;." --icon=Logo-Website.ico main_program.py

import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import sys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os 




#col_name=['URL']
#df_url_dataset = pd.read_excel('Data-Pipeline/Dataset-Raw/URLDataTwitter2_shuffled.xlsx', names=col_name)
#print(df_url_dataset)


folder_path = r'C:\Users\User\Documents\Python_Developing\Python\Freie-Wirtschaft-Crawler\Datasets\RAW'
file_names = os.listdir(folder_path)

data_frames = []

for file_name in file_names:
    if file_name.endswith('.xlsx'):  # Filter Excel files
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_excel(file_path, usecols=["EXTERNAL_URL"])
        data_frames.append(df)

concatenated_df = pd.concat(data_frames, ignore_index=True)

print("Initial DataFrame shape:", concatenated_df)

#concatenated_df.dropna(inplace=True)

print("DataFrame shape after dropping empty rows:", concatenated_df.shape)


column_name = "EXTERNAL_URL"
string_to_drop = 'MORE THAN ONE EXTERNAL URL'

concatenated_df = concatenated_df[concatenated_df[column_name] != string_to_drop]

print("DataFrame shape after dropping rows based on strings:", concatenated_df.shape)

string_to_drop = 'NO EXTERNAL URL'

concatenated_df = concatenated_df[concatenated_df[column_name] != string_to_drop]

print("DataFrame shape after dropping rows based on strings:", concatenated_df.shape)

concatenated_df.drop_duplicates(subset=column_name, inplace=True)

print("DataFrame shape after dropping duplicates:", concatenated_df.shape)

concatenated_df = concatenated_df.sample(frac=1).reset_index(drop=True)

print("Final DataFrame shape after shuffling:", concatenated_df.shape)

print(concatenated_df)

url_list = concatenated_df['EXTERNAL_URL'].tolist()

print(url_list)

path_to_main_folder = open('Paths/path_to_main_folder.txt', 'r')
path_folder = path_to_main_folder.read() #read whole file to a string
path_to_main_folder.close()
print('Path to main folder: ', path_folder)

path_to_webdriver = open('Paths/path_to_webdriver.txt', 'r')
path_webdriver = path_to_webdriver.read()
path_to_webdriver.close()
path_webdriver2 = path_webdriver + 'chromedriver'
print('Path to webdriver: ', path_webdriver2)

options = webdriver.ChromeOptions() 
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--headless')
driver = webdriver.Chrome(options=options, executable_path=path_webdriver2)
driver.set_page_load_timeout(30)

url_list = [str(item) for item in url_list]

external_urls = []
print(url_list)


for row in url_list:
    try:
        time.sleep(2)
        driver.get(row)
        driver.implicitly_wait(10)
        current_url = driver.execute_script("return window.location.href;")
        print(current_url)
        external_urls.append(current_url)
    except Exception as e:
        print("Timeout reached for URL:", row)
        external_urls.append('URL Crawling Failed')

    
df_external_urls = pd.DataFrame(external_urls)
df_external_urls.columns = ['URL']

df_external_urls.to_excel('Data-Pipeline/Dataset-Final/Twitter_URL_Data_GET_URL_DATA_300823.xlsx', index=False)