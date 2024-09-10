import time

import pymongo

from Utils.bs4_selenium import ChromeBrowser
from Utils.logger import logger
from constants import base_url, hard_drive

i = 1

mongo_url = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(mongo_url)
db = client['joe']
collection = db['hard_drives']

browser = ChromeBrowser()
browser.get_url(hard_drive)
logger.info(hard_drive)

# dir = directory_creator(save_path + 'monitors/')

while True:
    logger.info(f"Page:{i}")
    soup_page = browser.get_current_soup()
    page_URL = browser.driver.current_url

    items = soup_page.find_all("div", class_="productInner_UCJ1nUFwhh")

    for item in items:
        # try:
        #     hover_item = browser.driver.find_element(By.CSS_SELECTOR, f'div.product_UCJ1nUFwhh:nth-child({i})')
        #     browser.driver.execute_script("arguments[0].scrollIntoView(true);", hover_item)
        # except Exception:
        #     pass

        a_tag = item.find('a', class_='title_UCJ1nUFwhh')
        MRC = a_tag['href'].replace('/c/product/', '').split("/")[0]
        link = base_url + a_tag['href']
        title = a_tag.find('span').text
        img = item.find('img')['src']
        try:
            price_sec = item.find('div', class_='price_x6DXwdw1Fb')
            main_price = price_sec.select_one("span span").text
            af_z_price = price_sec.select_one("span sup").text
            price = main_price + '.' + af_z_price
        except Exception:
            price = "Not available"
        # product page
        # browser.get_url(link)
        # product_page_soup = browser.get_current_soup()
        # UPC_Section = product_page_soup.find('div', class_='upc_UbV5SNP5Eo')
        # UPC_code = UPC_Section.find('div', class_='js-injected-html').text.replace('UPC: ', '')
        # try:
        #     weight, images_links = get_product_UPC_data(UPC_code)
        # except Exception:
        #     weight = "Not available"
        #     images_links = []
        logger.info(title)
        # file_name = make_cleaned_filename(title)
        # for image in images_links:
        #     download_image(img, dir + f'{file_name}_{images_links.index(image)}')

        temp_dic = {
            'UPC': None,
            'MRC': MRC,
            'title': title,
            'link': link,
            'price': price,
            'weight': None,
            'img_link': None,
        }
        try:
            collection.insert_one(temp_dic)
        except Exception:
            logger.error('The Item has been saved in database')
    i += 1

    browser.get_url(hard_drive + f'/pn/{i}')
    time.sleep(10)
    page_URL = browser.driver.current_url
    logger.info(page_URL)
    if page_URL == hard_drive:
        break
    time.sleep(5)

    # wait = WebDriverWait(browser.driver, 10)
    # try:
    #     button = wait.until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, '.list_Mq9n1iP4rq > li:nth-child(11) > a:nth-child(1)')))
    #
    #     # Scroll to the button using JavaScript
    #     browser.driver.execute_script("arguments[0].scrollIntoView(true);", button)
    #
    #     # Click the button if it is clickable
    #     if button.is_enabled() and button.is_displayed():
    #         button.click()
    #         time.sleep(random.randint(10, 25))

browser.driver.close()