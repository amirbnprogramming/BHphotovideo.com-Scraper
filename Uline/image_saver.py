import random

import requests
import os
import re

from pymongo import MongoClient

from Uline.constants import user_agents

save_directory = "images/"

mongo_uri = 'mongodb://localhost:27017/'
database_name = 'Uline'
collection_name = 'Products'

client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]


def get_request(URL):
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

def model_number_extractor(url):
    match = re.search(r"\/([^\/?]+)\?", url)
    if match:
        image_id = match.group(1)
        return image_id


def download_images(url, save_directory):
    response = get_request(url)
    if response.status_code == 200:
        model_no = model_number_extractor(url)
        save_path = os.path.join(save_directory, f"{model_no}.webp")
        # Save the image
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {model_no}.webp successfully!")
    else:
        print(f"Failed to download {url}")


# Example usage

records = collection.find()
for record in records:
    url_image = record['img_link']
    download_images(url_image, save_directory)
