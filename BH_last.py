import random
import re
import time

from pymongo import MongoClient

from Utils.bs4_selenium import ChromeBrowser

def extract_number_and_symbols(price_str):
    pattern = r'([^\d\s]+)\s*([\d,]+(?:\.\d+)?)'
    match = re.match(pattern, price_str)
    if match:
        symbol = match.group(1)
        number = match.group(2).replace(',', '')  # Remove commas from the number
        return symbol, number
    else:
        return None, None



mongo_uri = 'mongodb://localhost:27017/'
database_name = 'joe'
new_collection_name = 'bhphotovideo_data'

client = MongoClient(mongo_uri)
db = client[database_name]
new_collection = db[new_collection_name]

records = new_collection.find()

browser = ChromeBrowser()
pattern = r'MFR\s+#(.+)'

for record in records:
    link = record['link']
    browser.get_url(link)
    soup = browser.get_current_soup()
    time.sleep(3)
    try:
        codes = "".join(soup.find('div', class_='code_kcQ1qlyqn6').text.split("<!-- -->"))
        matches = re.search(pattern, codes)
        if matches:
            mfr_code = matches.group(1)
        else:
            mfr_code = None
    except Exception as e:
        mfr_code = None

    try:
        description = soup.find('div', class_='overviewDescription_OMS5rN7R1Z js-injected-html').text.replace('<b>',
                                                                                                              '').replace(
            '<strong>', '')
    except Exception as e:
        description = None

    try:
        price_section = soup.find('div', class_='pricesContainer__9gLfjPSjp').find('div').text
        symbole, price_number = extract_number_and_symbols(price_section)
    except Exception as e:
        symbole = None
        price_number = None

    temp_dic = {'MFR-Code': mfr_code, 'Description': description, 'price': price_number, 'Price_Unit': symbole}
    result = new_collection.update_many({'_id': record['_id']}, {"$set": temp_dic})

    print(f'link:{link}')
    print(f'MFR:{mfr_code}')
    print(f'Description lenght:{len(description) if description is not None else "Nothing"}')
    print(f'price:{price_number}')
    print(f'Price_Unit:{symbole}')
    # try:
    #     manufacturer = record['title'].split(' ')[0]
    # except Exception as e:
    #     manufacturer = None
    # temp_dic = {'Manufacturer':manufacturer}
    # 'MFR-Code': mfr_code, 'Description': description,
