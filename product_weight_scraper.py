import re
import time

from selenium.webdriver.common.by import By


def extract_weights(text):
    # Enhanced regex pattern to extract weights with various units
    pattern = r'(\d+\.?\d*)\s*(lbs|lb|pounds|g|oz?)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    extracted_weights = [f"{float(value)}{unit}" for value, unit in matches]
    return extracted_weights



def weight_image_finder(soup):
    weights = []
    img_div = soup.find('div', class_='mainImageContainer_qRCujnFA4G')

    if img_div:
        img = img_div.find('img')['src']
    else:
        img = None

    try:
        button = driver.find_element(By.CSS_SELECTOR, '.nav_nJK1pHjy8m > li:nth-child(2) > div:nth-child(1) > a:nth-child(1)')
        button.click()
        soup = get_current_soup(driver)
    except Exception as e:
        pass

    info = soup.find_all('tr')
    if len(info) == 0:
        info = soup.find_all('span')
    for span in info:
        weights.extend(extract_weights(span.text))
    weight = sorted(weights)[0] if weights else None

    return weight, img










