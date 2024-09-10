import csv
import random
import re

import requests
import os

from bson import ObjectId
from pymongo import MongoClient

from constants import user_agents
from test import resize_and_pad

mongo_uri = 'mongodb://localhost:27017/'
database_name = 'joe'
collection_name = 'bhphotovideo_data'

client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# collection.update_many(
#     {},  # Filter: an empty dictionary matches all documents in the collection
#     { '$unset': { 'photo_dowload_state': "" } }  # Unset the 'columnName' field
# )
#
# collection.update_many({}, { "$set": { "photo_download_state": False} })

input_directory = 'Images/BH/main/'

output_file = 'Images/bhphoto_registery.csv'
header_text = 'Command^CAGE^Contract^Part Number^Image Type^Image Name^'


def clean_value(value):
    """Convert value to string, replace None with empty string, and remove quotes."""
    if value is None:
        return ''
    value = str(value)
    value = re.sub(r"[\"\'\^\|]", " ", value)
    return value.replace('\n', '')


def convert_to_filename(string):
    # Replace special characters with underscores
    cleaned_string = re.sub(r'[^\w\s-]', '', string.strip())
    # Replace double quotes with whitespace
    cleaned_string = cleaned_string.replace('"', ' ')
    # Replace consecutive whitespace with a single space
    cleaned_string = re.sub(r'\s+', ' ', cleaned_string)
    # Trim leading and trailing whitespace
    cleaned_string = cleaned_string.strip()
    # Convert spaces to underscores
    cleaned_string = cleaned_string.replace(' ', '_')
    # Convert to lowercase
    cleaned_string = cleaned_string.lower()
    return cleaned_string


def get_request(url):
    time_sent = 0
    while time_sent < 10:
        user_agent = random.choice(user_agents)
        headers = {'User-Agent': user_agent}
        try:
            res = requests.get(url, headers=headers)
            res.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        time_sent += 1
    return res


def download_images(url, name):
    response = get_request(url)
    if response.status_code == 200:
        # Extract the filename from the URL
        file_format = url.split("/")[-1].split('.')[-1]
        saved_file_name = name + '.' + file_format
        saved_path = input_directory + name + '.' + file_format
        # Save the image
        with open(saved_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {saved_file_name} successfully!")
        status = True
    else:
        print(f"Failed to download {url}")
        status = False
        file_format = None

    return status, file_format


with open(output_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='^', quoting=csv.QUOTE_MINIMAL)
    file.write(header_text + '\n')

    records = collection.find()
    for record in records:
        if record['photo_download_state'] == False or record['photo_download_state'] is None:
            url_image = 'https://www.bhphotovideo.com' + record['img_link']
            mrc = record['MRC']
            print(mrc)
            file_name = convert_to_filename(record['title'])
            status, format = download_images(url_image, file_name)
            if status and format is not None:
                """Make full size 500*500"""
                target_size = 480
                frame_size = 10
                output_directory = 'Images/BH/full_size/'
                input_path = os.path.join(input_directory, file_name + '.' + format)
                output_path = os.path.join(output_directory, file_name + '_fullsize.' + format)
                resize_and_pad(input_path, output_path, target_size, frame_size)
                print("full size 500*500 saved")

                """CSV record saving"""
                row = [
                    'ADD',
                    '9X4Y0',
                    'MARKETPLACE_9X4Y0',
                    mrc,
                    '1',
                    file_name + '_fullsize.' + format,
                ]
                writer.writerow(row)

                print(f'Data has been written to CSV')

                """Make thumbnail"""
                target_size = 140
                frame_size = 10
                output_directory = 'Images/BH/thumbnails/'
                input_path = os.path.join(input_directory, file_name + '.' + format)
                output_path = os.path.join(output_directory, file_name + '_thumb.' + format)
                resize_and_pad(input_path, output_path, target_size, frame_size)
                print("Thumbnail 160*160 saved")

                """CSV record saving"""
                row = [
                    'ADD',
                    '9X4Y0',
                    'MARKETPLACE_9X4Y0',
                    mrc,
                    'T',
                    file_name + '_thumb.' + format,
                ]
                writer.writerow(row)

                print(f'Data has been written to CSV')
                collection.update_one({'_id': record['_id']}, {'$set': {'photo_download_state': True}})
            else:
                print("Could not downloaded")
            print("**********************************")
client.close()
