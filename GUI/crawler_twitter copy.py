import os
import sys
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
import sys
from selenium.webdriver.support import expected_conditions as EC
import time
from data_manager import crawler_temporary_storage
import random


def crawl_twitter(driver, url, n):
	'''
	Function that crawls the twitter page
	'''
	
	driver.get(url)
	driver.implicitly_wait(15)
	status_urls_list = []
	text_list = []

	# Scroll down the twitter profile and collect status urls
	for i in range(n):
		random_number = random.randrange(1, 6)
		time.sleep(random_number)
		print(f"Number of crawls: {i}")

		element_body = driver.find_element(By.TAG_NAME, 'a')
		elems = driver.find_elements(By.XPATH, '//a[@href]')

		for elem in elems:
			href = elem.get_attribute('href')
			href = str(href)
			if 'status' in href and 'photo' not in href and 'analytics' not in href:
				status_urls_list.append(href)
			else:
				pass
		elems2 = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')

		for elem2 in elems2:
			tweet_text = elem2.text
			print(tweet_text)
			text_list.append(tweet_text)
		
		element_body.send_keys(Keys.PAGE_DOWN)
	
	# Remove duplicates from crawled list of status urls
	status_urls_list = list(dict.fromkeys(status_urls_list))
	
	# Start crawling detail views
	status_text_list = []
	status_external_url_list = []

	external_url_list = []

	for status_url in status_urls_list:
		driver.get(status_url)
		driver.implicitly_wait(10)
		current_url = driver.execute_script("return window.location.href;")



		random_number = random.randrange(2, 4)
		time.sleep(random_number)
		driver.get(status_url)
		try:
			status_data = wait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetText"]')))
			status_text = status_data.text
			status_text = status_text.replace('\n',' ')
			print(status_text)
			status_text_list.append(status_text)
		except:
			status_text_list.append('NO TWEET TEXT') 

		try:
			status_text = driver.find_elements(By.XPATH, '//a[@href]')
			all_status_urls = []
			for elem in status_text:
				href = elem.get_attribute('href')
				print(href)
				all_status_urls.append(str(elem.get_attribute('href')))

			all_status_urls = list(dict.fromkeys(all_status_urls))            

			if any(item.startswith('https://t.co') for item in all_status_urls):
				external_urls = []
				for line in all_status_urls:
					if line.startswith('https://t.co'):
						external_urls.append(line) # here driver should get url from t.co urls
					else:
						pass
				if len(external_urls) > 1:
					more_than_two_links = ' '.join(external_urls)
					status_external_url_list.append(more_than_two_links)
				else:
					for line in external_urls:
						status_external_url_list.append(line)
			else: 
				status_external_url_list.append('NO EXTERNAL URL')
		except:
			status_external_url_list.append('NO EXTERNAL URL')        

	# Store the data in temporary storage folder
	temp_stor = crawler_temporary_storage(status_urls_list, status_text_list, status_external_url_list) 
	return status_urls_list, status_text_list, status_external_url_list