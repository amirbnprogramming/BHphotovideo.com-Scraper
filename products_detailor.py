import time

from pymongo import MongoClient

from UPC import get_product_UPC_data
from Utils.bs4_selenium import ChromeBrowser
from detailor_1 import get_product_weight

mongo_uri = 'mongodb://localhost:27017/'  # Replace with your MongoDB URI
database_name = 'joe'  # Name of your database
new_collection_name = 'bhphotovideo_data'  # Name of the new collection

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
new_collection = db[new_collection_name]

browser = ChromeBrowser()


def get_upc_code(link_page):
    # product page
    browser.get_url(link_page)
    product_page_soup = browser.get_current_soup()
    try:
        UPC_Section = product_page_soup.find('div', class_='upc_UbV5SNP5Eo')
        UPC_code = UPC_Section.find('div', class_='js-injected-html').text.replace('UPC: ', '')
    except Exception as e:
        UPC_code = None
    return UPC_code


records = new_collection.find()
for record in records:
    if record['weight'] is None:
        link = record['link']
        # UPC_code = get_upc_code(link)
        title = record['title']
        weight = get_product_weight(title)
        # if UPC_code is not None:
        #     weight, images = get_product_UPC_data(UPC_code)
        # else:
        #     weight, images = None, None
        print(link)
        # print(UPC_code)
        # record['UPC'] = UPC_code
        # record['weight'] = weight
        # record['img_link'] = images
        # Save the updated document back to the collection
        new_collection.update_one({'_id': record['_id']}, {'$set': {'weight': weight}})
        time.sleep(5)
client.close()