import time
import pandas as pd
import sys
import requests 
import html2text 
import re
from bs4 import BeautifulSoup
import nltk
import newspaper
import pickle 
from collections import Counter 
import csv
import os
from algorithms import classify

nltk.download('punkt')


def CleanString(text):
    '''
    Use regex to clean crawled text
    '''
    filtered_text = text.replace('\n', ' ') # Replacing next line char
    filtered_text = filtered_text.replace('  ', ' ') # Replacing two spaces
    filtered_text = re.sub(r'[^ ]+\.[^ ]+',' ', filtered_text) # Remove all strings with url path
    filtered_text = re.sub(r'[^\/]+$',' ', filtered_text) # Remove all strings with slash
    filtered_text = re.sub(r'http://\S+|https://\S+', ' ', filtered_text, flags=re.MULTILINE) # Remove html links
    filtered_text = re.sub(r'\/', ' ', filtered_text) # remove all forward slashes
    filtered_text = re.sub(r'\b\w{1,3}\b', ' ', filtered_text) # Remove strings with less than 4 characters
    filtered_text = re.sub(r'\b\w{17,10000000}\b', ' ', filtered_text) # remove strings larger than 17 characters
    filtered_text = re.sub(r'[^\w\s.,\'"!?]+', ' ', filtered_text) # Remove all symbols except dots, commas, quotation marks, exclamation marks and question marks
    filtered_text = re.sub(r'\s+', ' ', filtered_text, flags = re.I) # Remove multiple spaces
    filtered_text = re.sub(r'^\s+', '', filtered_text) # Remove spaces at the beginning of string
    filtered_text = re.sub(r'\s+$', '', filtered_text) # Remove spaces at the end of the string
    return filtered_text


def CleanAuthor(text):
    '''
    Clean authors of crawled news article
    '''
    authors = str(text)
    authors = authors.replace('[\'', '')
    authors = authors.replace('\']', '')
    authors = authors.replace('\', \'', ' & ')
    authors = authors.replace('[]', 'None')
    return authors


def CleanArticleText(text):
    '''
    Clean text of crawled news article
    '''
    article_text = str(text)
    article_text = article_text.replace('\n', ' ')
    article_text = re.sub(' +', ' ', article_text)
    return article_text


def ConvertString(string):
    '''
    Convert string to list
    '''
    li = list(string.split(' '))
    return li


def ConvertTuple(tup):
    '''
    Convert tuple to string
    '''
    str =  ' '.join(tup)
    return str
    

def feature_extractor(word):
    features = {}
    features['suffix'] = word[-3:]
    features['prefix'] = word[:3]
    return features
    

class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        if name == 'ClassifierBasedEnglishTagger':
            from algorithms import ClassifierBasedEnglishTagger
            return ClassifierBasedEnglishTagger
        if name == 'ClassifierBasedGermanTagger':
            from algorithms import ClassifierBasedGermanTagger
            return ClassifierBasedGermanTagger
        return super().find_class(module, name)


algorithm_folder = "Algorithms"

if getattr(sys, 'frozen', False):
    main_folder = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

else:
    main_folder = os.path.dirname(os.path.abspath(__file__))

# Load German word tagger
nltk_german_wordtype_classifier_filename = "nltk_german_wordtype_classifier_data.pkl"
nltk_german_wordtype_classifier_filepath = os.path.join(main_folder, algorithm_folder, nltk_german_wordtype_classifier_filename)
tagger_de = CustomUnpickler(open(nltk_german_wordtype_classifier_filepath, 'rb')).load()


# Load English word tagger
nltk_english_wordtype_classifier_filename = "nltk_english_wordtype_classifier_data.pkl"
nltk_english_wordtype_classifier_filepath = os.path.join(main_folder, algorithm_folder, nltk_english_wordtype_classifier_filename)
tagger_en = CustomUnpickler(open(nltk_english_wordtype_classifier_filepath, 'rb')).load()


# Load language classifier into program 

category_classifier_file = 'sklearn_category_classifier_en.pkl'
path_to_category_classifier = os.path.join(main_folder, algorithm_folder, category_classifier_file)
category_model_en = pickle.load(open(path_to_category_classifier, 'rb'))


# Load source list into program

sources_dataset_filename = "Sources-Dataset.xlsx"
links_and_sources_folder = "Links-and-Sources"
path_to_sources_dataset = os.path.join(main_folder, links_and_sources_folder, sources_dataset_filename)
df_sources = pd.read_excel(path_to_sources_dataset)
df_sources.drop_duplicates(subset='source_url', inplace=True)
print(df_sources)


# Start crawling articles 

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

def data_pipeline_step1(url):
    article_url_list = []
    article_source_list = []
    article_title_list = []
    article_text_list = []
    article_author_list = []
    article_publish_date_list = []
    article_language_list = []
    article_first_category_list = []
    article_first_category_prob_list = []
    article_second_category_list = []
    article_second_category_prob_list = []
    article_tags_list = []
    
    try:
        article_url_list.append(url)
        time.sleep(2)
        page = requests.get(url, headers=headers, timeout=30)
        #page.encoding
        html_code = page.content
        bsObj = BeautifulSoup(html_code, features='html.parser')
        page_encoding = bsObj.original_encoding
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        text_from_html = h.handle(html_code.decode(page_encoding, 'ignore'))
        text_from_html_cleaned = CleanString(text_from_html)
        splitted_words = text_from_html_cleaned.split()
        first_50_words = splitted_words[:100]
        text_from_html_cleaned = ' '.join(first_50_words)
        probability, predicted_class = classify(text_from_html_cleaned)
        predicted_language_class = predicted_class[0][0]
        print(predicted_language_class)
        article_language_list.append(predicted_language_class)
    except Exception as e: 
        print(e)
        print('ERROR: Crawling failed!')
        article_language_list.append('ERROR: Crawling Failed')
        page = 'NA'
        html_code = 'NA' 
        text_from_html = 'NA'
        text_from_html_cleaned = 'NA'

    # Extract data from webpages
    try:
        html_content = page.text
        if predicted_language_class == 'German':
            article = newspaper.Article('', language='de')
        else:
            article = newspaper.Article('', language='en')

        article.set_html(html_content)
        article.parse()

        try:
            article_title_list.append(str(article.title))
        except Exception as e: 
            print(e)
            article_title_list.append('NA')

        try:
            article_text = CleanArticleText(article.text)
            print(article_text)
            if len(article_text) == 0: # Check if text extraction worked and if string is empty
                article_text_list.append(text_from_html_cleaned) # If string is empty, append cleaned content from request
            else:
                article_text_list.append(article_text)
        except Exception as e:
            print(e)
            article_text_list.append('NA')

        try:
            authors = CleanAuthor(article.authors)
            article_author_list.append(authors)
        except Exception as e:
            print(e)
            article_author_list.append('NA')

        try: 
            article_publish_date_list.append(str(article.publish_date))
        except Exception as e:
            print(e)
            article_publish_date_list.append('NA')

    except Exception as e:
        print(e)
        print('ERROR: Crawler failed to extract data!')
        article_title_list.append('ERROR')
        article_text_list.append('ERROR')
        article_author_list.append('ERROR')
        article_publish_date_list.append('ERROR')

    # Extract tags from article text or from request content
    try:
        tags_list = []
        if predicted_language_class == 'German':
            if len(article_text) == 0:
                converted_text_from_html_cleaned = ConvertString(text_from_html_cleaned)
                keywords = tagger_de.tag(converted_text_from_html_cleaned)
            else:
                converted_article_text = ConvertString(article_text)
                keywords = tagger_de.tag(converted_article_text)
            nomen_tags_NN = [t for t in keywords if t[1] == 'NN']
            nomen_tags_FM = [t for t in keywords if t[1] == 'FM']
            nomen_tags_NE = [t for t in keywords if t[1] == 'NE']
            keywords = nomen_tags_FM + nomen_tags_NN + nomen_tags_NE
            print(keywords)

        elif predicted_language_class == 'English':
            if len(article_text) == 0:
                converted_text_from_html_cleaned = ConvertString(text_from_html_cleaned)
                keywords = tagger_en.tag(converted_text_from_html_cleaned)
            else:
                converted_article_text = ConvertString(article_text)
                keywords = tagger_en.tag(converted_article_text)
            keywords = [t for t in keywords if t[1].startswith('N')]
            print(keywords)
        else:
            pass

        tags_list.extend(keywords)
        Total_text = [a for a,b in tags_list]
        Keywords_counted2 = Counter(Total_text)
        print(Keywords_counted2)
        keywords_top20 = Keywords_counted2.most_common(30)
        keywords_top20 = [a for a,b in keywords_top20]
        endstring_top20 = ConvertTuple(keywords_top20)
        article_tags_list.append(endstring_top20)
    except Exception as e:
        print(e)
        print('ERROR: Tagging failed')
        article_tags_list.append('NA')

    # Extract name of source
    try:
        for index, row in df_sources.iterrows():
            source_detected = False
            if url.startswith(row['source_url']):
                article_source_list.append(row['source_name'])
                source_detected = True
                break
        if not source_detected:
            article_source_list.append('NA')
    except Exception as e:
        print(e)
        print('ERROR: Source detection failed!')
        article_source_list.append('ERROR: Source detection failed!')

    # extract class names and their probabilities
    try:
        if len(article_text) == 0: # Check if text extraction worked and if string is empty
            predicted_prob = category_model_en.predict_proba([text_from_html_cleaned])[0]
            predicted_prob = predicted_prob * 100
            class_names = category_model_en.classes_
            class_probabilities = dict(zip(class_names, predicted_prob))

            # extract first and second best predicted class with their probabilities
            predicted_class = class_names[predicted_prob.argmax()]
            print('1st predicted class: ', predicted_class)
            article_first_category_list.append(predicted_class)

            predicted_probability = class_probabilities[predicted_class]
            print('Probability 1st class: ', predicted_probability)
            article_first_category_prob_list.append(predicted_probability)

            second_predicted_class = class_names[predicted_prob.argsort()[-2]]
            print('2nd predicted class: ', second_predicted_class)
            article_second_category_list.append(second_predicted_class)

            second_predicted_probability = class_probabilities[second_predicted_class]
            second_predicted_probability = second_predicted_probability * 100
            print('Probability 2nd class: ', second_predicted_probability) # If string is empty, append cleaned content from request
            article_second_category_prob_list.append(second_predicted_probability)
        else:
            predicted_prob = category_model_en.predict_proba([article_text])[0]
            predicted_prob = predicted_prob * 100
            class_names = category_model_en.classes_
            class_probabilities = dict(zip(class_names, predicted_prob))

            # extract first and second best predicted class with their probabilities
            predicted_class = class_names[predicted_prob.argmax()]
            print('1st predicted class: ', predicted_class)
            article_first_category_list.append(predicted_class)

            predicted_probability = class_probabilities[predicted_class]
            print('Probability 1st class: ', predicted_probability)
            article_first_category_prob_list.append(predicted_probability)

            second_predicted_class = class_names[predicted_prob.argsort()[-2]]
            print('2nd predicted class: ', second_predicted_class)
            article_second_category_list.append(second_predicted_class)

            second_predicted_probability = class_probabilities[second_predicted_class]
            #second_predicted_probability = second_predicted_probability * 100
            print('Probability 2nd class: ', second_predicted_probability)
            article_second_category_prob_list.append(second_predicted_probability)
    except Exception as e:
        print(e)
        print('ERROR: Classification of category failed!')
        article_first_category_list.append('NA')
        article_first_category_prob_list.append('NA')
        article_second_category_list.append('NA')
        article_second_category_prob_list.append('NA')

    return {
        'article_url': url,
        'article_source': article_source_list[0] if article_source_list else None,
        'article_author': article_author_list[0] if article_author_list else None,
        'article_title': article_title_list[0] if article_title_list else None,
        'article_text': article_text_list[0] if article_text_list else None,
        'article_publish_date': article_publish_date_list[0] if article_publish_date_list else None,
        'article_language': article_language_list[0] if article_language_list else None,
        'article_first_category': article_first_category_list[0] if article_first_category_list else None,
        'article_first_category_prob': article_first_category_prob_list[0] if article_first_category_prob_list else None,
        'article_second_category': article_second_category_list[0] if article_second_category_list else None,
        'article_second_category_prob': article_second_category_prob_list[0] if article_second_category_prob_list else None,
        'article_tags': article_tags_list[0] if article_tags_list else None
    }