import os
import sys
import pandas as pd
import sys
import pandas as pd
import io
from crawler_twitter import crawl_twitter
from data_manager import get_crawling_sources, crawler_final_storage
import undetected_chromedriver as uc
from datetime import datetime



class CrawlingOutputStream(io.TextIOBase):
	'''
	Class that gets the queue data from crawling output, which will be printed in the GUI terminal
	'''
	def __init__(self, queue):
		super().__init__()
		self.queue = queue

	def write(self, s):
		self.queue.put(s)
		


def initialize_webdriver():
	'''
	Function that initializes the webdriver 
	'''
	script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
	assets_folder = "assets"
	webdriver_filename = "chromedriver"
	webdriver_path = os.path.join(script_directory, assets_folder, webdriver_filename)
	options = uc.ChromeOptions() 
	options.add_argument('--blink-settings=imagesEnabled=false')
	driver = uc.Chrome(driver_executable_path=webdriver_path, options=options, headless=False, use_subprocess=False)
	driver.set_page_load_timeout(30)
	return driver



def crawling_process(queue):
	'''
	Main function of the data crawling process
	'''
	sys.stdout = CrawlingOutputStream(queue)
	
	df_url_dataset = get_crawling_sources()
	print(df_url_dataset)
	
	final_data_results = []


	# Loop through link sources and crawl website

	for link in df_url_dataset.iterrows():
		url = link[1]['Url']
		no_of_crawls = link[1]['No_of_scrolls']
		print(f'Link-Source {url}')

		driver = initialize_webdriver()
		
		try:
			if url.startswith('https://twitter.com'):
				print('Twitter')
				data_results = crawl_twitter(driver, url, no_of_crawls)
				final_data_results.extend(data_results)
				driver.quit()
			else:
				print('ERROR: No crawler associated with this link!')
				driver.quit()
		except Exception as e:
			print(e)
			print('ERROR: Crawling failed!')
			driver.quit()

	# Save final data file to Storage-Final

	print(final_data_results)

	try: 
		df = pd.DataFrame(final_data_results)

		headers = [
			'URL', 'Source', 'Author', 'Title', 'Full_Text', 
			'Date', 'Language', '1st_Category', 
			'1st_Category_Probability', '2nd_Category', 
			'2nd_Category_Probability', 'Tags'
		]

		df.columns = headers
		print(df)

		main_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
		data_crawling_folder = "Data-Crawling"
		final_storage_folder = "Storage-Final"
		time_now = datetime.now()
		time_formatted = time_now.strftime('%d.%m.%Y-%H:%M:%S')
		filename = f"Final_Crawling_{time_formatted}.xlsx"
		filepath = os.path.join(main_folder, data_crawling_folder, final_storage_folder, filename)

		df.to_excel(filepath, header=True, index=None)
	except Exception as e:
		print("Error occurred while saving the file:", str(e))
	
	driver.quit()
		
