import random
import time

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

from Utils.bs4_selenium import ChromeBrowser
from constants import user_agents, uline_main_page, base_url

# data base installation
mongo_uri = 'mongodb://localhost:27017/'
database_name = 'Uline'

client = MongoClient(mongo_uri)
db = client[database_name]


class Uline:
    def __init__(self):
        self.links = {}
        self.main_url = uline_main_page
        # self.browser = ChromeBrowser()

    def get_request(self, URL):
        time_sent = 0
        while time_sent < 10:
            user_agent = random.choice(user_agents)
            headers = {'User-Agent': user_agent}
            try:
                res = requests.get(URL, headers=headers)
                res.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
            time_sent += 1
        return res

    def super_categories_scraper(self):
        self.get_deeper_link(self.main_url, 'super_categories')

    def get_deeper_link(self, url, collection_name):
        child_links = []
        # new_collection = db[collection_name]
        response = self.get_request(url)
        if response is not None:
            soup = BeautifulSoup(response.text, 'html.parser')
            # find all a tags
            links = soup.select('#bodycontent  div.cssstaticpages  div:nth-of-type(2) a')
            for a_tag in links:
                if a_tag.get('href') is not None:
                    link = base_url + a_tag.get('href')
                else:
                    link = None

                if a_tag.text is not None and a_tag.text != "":
                    title = a_tag.text

                    print(f'Title:{title.strip()}')
                    print(f'Link:{link}')

                    # if new_collection.find_one({'title': title}) is None:
                    #     new_collection.insert_one({'title': title, 'link': link, 'scraped': False, 'depth': False})
                    # self.links[title] = link
                    child_links.append(link)
        return child_links, response.text


# uline_scraper = Uline()
# uline_scraper.super_categories_scraper()

# new_collection = db['categories']
# update_result = new_collection.update_many(
#     {},  # Empty filter matches all documents
#     {"$set": {'depth': False, 'scraped': False, 'child_links':[]}}
# )


# new_collection = db['categories']
#
# super_categories = new_collection.find({'scraped': False})
# for cat in super_categories:
#     link = cat['link']
#     title = cat['title']
#     if link is not None and link != "" and title is not None and title != "":
#         print(f'**** {link} ****')
#         result = uline_scraper.get_deeper_link(link, 'categories')
#         new_collection.update_many({'title': title}, {"$set": {'scraped': True}})
#         if len(result) > 0:
#             new_collection.update_many({'title': title}, {"$set": {'depth': True, 'child_links': result}})
#         print('**** end section ****')

#
# client = MongoClient(mongo_uri)
# db = client[database_name]
# base = db['target']
# source_collection = db['sources']
#
# base_items = base.find().skip(150)
# i=0
# for record in base_items:
#     array = record['childs']
#     for link in array:
#         if link is not None and 'AdvSearchResult' not in link and "javascript" not in link and "uline.com" in link and source_collection.find_one({"link":link}) is None:
#             if "comProduct" in link:
#                 link = link.replace("comProduct", 'com/Product')
#             result, response = uline_scraper.get_deeper_link(link, 'deep_links')
#
#             if len(result) > 0 and base.find_one({'link': link}) is None:
#                 base.insert_one({'link': link, 'childs': result})
#
#             elif len(result) == 0 and source_collection.find_one({'link': link}) is None:
#                 source_collection.insert_one({'link': link, 'source': response})
#             print(f'**** end section ({i}) ****')
#             i+=1
# client.close()
# print(i)