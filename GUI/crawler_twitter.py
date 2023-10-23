from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
import time
import random
from data_pipeline import data_pipeline_step1


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
		random_number = random.randrange(1, 3)
		time.sleep(random_number)
		print(f"Number of crawls: {i}")

		element_body = driver.find_element(By.TAG_NAME, 'a')
		elems = driver.find_elements(By.XPATH, '//a[@href]')

		for elem in elems:
			href = elem.get_attribute('href')
			href = str(href)
			if href.startswith("https://t.co"):
				status_urls_list.append(href)
				print(href)
			else:
				pass
		
		element_body.send_keys(Keys.PAGE_DOWN)
	
	# Remove duplicates from crawled list of status urls
	status_urls_list = list(dict.fromkeys(status_urls_list))

	results_list = []

	for status_url in status_urls_list:
		try:
			driver.get(status_url)
			driver.implicitly_wait(20)
			current_url = driver.execute_script("return window.location.href;")
			print(current_url)
			result_dict = data_pipeline_step1(current_url)
			results_list.append(result_dict)
		except Exception as e:
			print("\n Error occurred while getting links: \n", str(e))

	return results_list

		