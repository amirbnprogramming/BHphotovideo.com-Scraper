# data base installation
import re
import time

import undetected_chromedriver
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Uline.main import Uline
from Utils.bs4_selenium import ChromeBrowser

mongo_uri = 'mongodb://localhost:27017/'
database_name = 'Uline'

client = MongoClient(mongo_uri)
db = client[database_name]
source_collection = db['sources']
products = db['Products']

uline_scraper = Uline()
base_items = source_collection.find()


def mean_of_set(numbers):
    numbers_list = list(numbers)
    total_sum = sum(numbers_list)
    count = len(numbers_list)
    mean = total_sum / count if count > 0 else 0

    return mean


def extract_price_number(string):
    pattern = r'\$?(\d+\.\d+|\.\d+|\d+)'

    matches = re.findall(pattern, string)

    for match in matches:
        match = match.lstrip('$')
        number_float = float(match)

        number=number_float

    return number


def child_text_extractor(tag):
    childs = tag.find()
    if childs:
        child_texts = [child.get_text(strip=True) for child in childs]
        all_child_text = ' '.join(child_texts)
        return all_child_text


def page_detailor(sent_soup):
    title, description, img_link, price, weight = None, None, None, None, None
    # response = uline_scraper.get_request(url)
    soup = sent_soup
    price_set = []
    chart = soup.select_one('#dvChart table #tdChart table')
    # print(chart)
    if chart is not None:
        trs = chart.find_all('tr')
        # print(trs)
        for tr in trs:
            tds = tr.find_all('td')
            # print(tds)
            for td in tds:
                td_text = td.text.strip()
                if 'ADD' not in td_text and 'lsb' in td_text.lower() or 'lb' in td_text.lower() or 'wt' in td_text.lower():
                    weight_index = tds.index(td)
                    try:
                        weight_tag = trs[-1].find_all('td')[weight_index]
                        weight = child_text_extractor(weight_tag)
                    except Exception as e:
                        weight = None
                if '$' in td_text:
                    try:
                        price = extract_price_number(td_text)
                        price_set.append(float(price))
                        price = round(mean_of_set(price_set), 3)
                    except Exception as e:
                        price = None
        print(f'weight:{weight}')
        print(f'Price:{price}')

    try:
        title_section = soup.select_one('#dvTop #dvTitle')
        if title_section:
            title = title_section.get_text(strip=True)
            print(f'Title:{title}')
    except Exception as e:
        title = None
        print("The title was not found.")

    try:
        description_section = soup.find('div', id='dvCopy')
        if description_section:
            description = description_section.get_text(strip=True)
            print(f'Description:{description}')
    except Exception as e:
        description = None
        print("The decription was not found.")

    try:
        img_section = soup.find('div', id='dvImage')
        if img_section:
            img_link = img_section.find('img', class_='itemResultImage')['src']
            print(f'Img: {img_link}')
    except Exception as e:
        img_link = None
        print("The img was not found.")

    tmp_dic = {'title': title, 'description': description, 'img_link': img_link, 'price': str(price),
               'weight': str(weight)}
    return tmp_dic


# from sources to products
# for record in base_items:
#     detail = {}
#     url = record['link']
#     print(url)
#     response = uline_scraper.get_request(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     try:
#         chart = soup.select('#dvChart  table  tr  td  table a')
#         for a_tag in chart:
#             if a_tag.text:
#                 if 'ADD' not in a_tag.get_text():
#                     url = 'https://www.uline.com' + a_tag['href']
#                     model_no = a_tag.get_text()
#                     detail = page_detailor(url)
#                     detail['link'] = url
#                     detail['model_no'] = model_no
#                     if products.find_one({'model_no': model_no}) is None:
#                         products.insert_one(detail)
#     except Exception as e:
#         chart = None
#     if detail:
#         source_collection.update_one({'_id': record['_id']}, {'$set':{'scraped':True}})
#     else:
#         source_collection.update_one({'_id': record['_id']}, {'$set':{'scraped':False}})


# page_detailor('https://www.uline.com/Product/Detail/S-16975LID/Plastic-Bins/Divider-Box-Lid-9-x-6-5-8')

# not found price: '#btnSelect'
i = 1
none_price = products.find({'price': "None"})
browser = ChromeBrowser()

for product in none_price:
    print(f'************({i})************')
    url = product['link']
    print(url)
    browser.get_url(url)
    #

    try:
        pop_up = WebDriverWait(browser.driver, 1).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#modalClose'))
        )
        pop_up.click()
        time.sleep(3)
        print("Popup closed successfully")
    except Exception as e:
        pass
    try:
        select_tags = browser.driver.find_elements(By.TAG_NAME, 'select')
        for tag in select_tags:
            tag.click()
            tag.send_keys(Keys.ARROW_DOWN)
            tag.send_keys(Keys.ENTER)
            time.sleep(2)
    except Exception as e:
        pass
    try:
        button = WebDriverWait(browser.driver, 1).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnSelect'))
        )
        button.click()
    except TimeoutException:
        print("Button not found within the timeout period")

    soup = browser.get_current_soup()
    # response = uline_scraper.get_request(url)
    detail = page_detailor(soup)
    print(detail)

    products.update_one({'_id': product['_id']}, {
        '$set': {'title':detail['title'],'description': detail['description'],
                 'weight': detail['weight'],
                 'price': detail['price'],
                 'img_link': detail['img_link']}})
    # print(detail)
    i += 1
print(i)
client.close()
