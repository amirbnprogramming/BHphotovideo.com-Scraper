import random

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import re
import time

from Utils.bs4_selenium import ChromeBrowser
from product_weight_scraper import weight_image_finder

# Set up the Selenium WebDriver


mongo_uri = 'mongodb://localhost:27017/'  # Replace with your MongoDB URI
database_name = 'joe'  # Name of your database
new_collection_name = 'bhphotovideo_data'  # Name of the new collection

client = MongoClient(mongo_uri)
db = client[database_name]
new_collection = db[new_collection_name]

browser = ChromeBrowser()
records = new_collection.find()
for record in records:
    if record['weight'] is None or record['weight'] == "":
        link = record['link']
        title = record['title']
        print(title)
        weight, img = weight_image_finder(browser, link)
        print(weight)
        print(img)
        if weight is not None:
            new_collection.update_one({'_id': record['_id']}, {'$set': {'weight': str(weight)}})
        if img is not None:
            new_collection.update_one({'_id': record['_id']}, {'$set': {'img_link': img}})
        time.sleep(random.randint(5, 8))
client.close()

browser.driver.close()
