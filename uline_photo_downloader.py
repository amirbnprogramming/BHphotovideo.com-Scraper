import csv
import random
import re

import requests
from PIL import Image
from pymongo import MongoClient

from constants import user_agents

mongo_uri = 'mongodb://localhost:27017/'
database_name = 'Uline'
collection_name = 'Products'

client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

input_webp_directory = 'Images/Uline/webp/'
input_directory = 'Images/Uline/main/'

output_file = 'Images/uline_registery.csv'
header_text = 'Command^CAGE^Contract^Part Number^Image Type^Image Name^'

# collection.update_many({}, { "$set": { "photo_download_state": False} })

# collection.update_many(
#     {},  # Filter: an empty dictionary matches all documents in the collection
#     { '$unset': { 'photo_dowload_state': "" } }  # Unset the 'columnName' field
# )

def clean_value(value):
    """Convert value to string, replace None with empty string, and remove quotes."""
    if value is None:
        return ''
    value = str(value)
    value = re.sub(r"[\"\'\^\|]", " ", value)
    return value.replace('\n', '')


def convert_to_filename(string):
    cleaned_string = re.sub(r'[®©,]', '', string)
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
        saved_path = input_webp_directory + name + '.webp'
        # Save the image
        with open(saved_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {name + '.webp'} successfully!")
        status = True
    else:
        print(f"Failed to download {url}")
        status = False

    return status


def convert_webp_to_jpg(webp_file, jpg_file):
    try:
        # Open the WebP image file
        with Image.open(webp_file) as img:
            # Save as JPG format
            img.convert("RGB").save(jpg_file, "JPEG")
            print(f"Converted {webp_file} to {jpg_file}")
    except IOError:
        print(f"Cannot convert {webp_file}")


with open(output_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='^', quoting=csv.QUOTE_MINIMAL)
    file.write(header_text + '\n')

records = collection.find()
for record in records:
    try:
        url_image = record['img_link']
        if record['photo_download_state'] == True or record['photo_download_state'] is None and url_image is not None and "none" not in url_image and "javascript" not in url_image :
            model_no = record['model_no']
            title = record['title']
            print(model_no)
            if title == None:
                file_name = convert_to_filename(model_no)
            else:
                file_name = convert_to_filename(record['title'])

            with open(output_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter='^', quoting=csv.QUOTE_MINIMAL)

                """CSV record saving"""
                row = [
                    'ADD',
                    '9X4Y0',
                    'MARKETPLACE_9X4Y0',
                    model_no,
                    '1',
                    file_name + '_fullsize.jpg',
                ]
                writer.writerow(row)

                """CSV record saving"""
                row = [
                    'ADD',
                    '9X4Y0',
                    'MARKETPLACE_9X4Y0',
                    model_no,
                    'T',
                    file_name + '_thumb.jpg',
                ]
                writer.writerow(row)

            status = download_images(url_image, file_name)

            if status and format is not None:
                with open(output_file, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter='^', quoting=csv.QUOTE_MINIMAL)
                    """Convert Webp to JPG"""
                    webp_file = input_webp_directory + file_name + '.webp'
                    jpg_file = input_directory + file_name + '.jpg'
                    convert_webp_to_jpg(webp_file, jpg_file)

                    """Make full size 300*300"""
                    target_size = 280
                    frame_size = 10
                    output_directory = 'Images/Uline/full_size/'
                    input_path = os.path.join(input_directory, file_name + '.jpg')
                    output_path = os.path.join(output_directory, file_name + '_fullsize.jpg')
                    resize_and_pad(input_path, output_path, target_size, frame_size)
                    print("full size 300*300 saved")

                    """CSV record saving"""
                    row = [
                        'ADD',
                        '9X4Y0',
                        'MARKETPLACE_9X4Y0',
                        model_no,
                        '1',
                        file_name + '_fullsize.jpg',
                    ]
                    writer.writerow(row)

                    print(f'Data has been written to CSV')

                    """Make thumbnail"""
                    target_size = 140
                    frame_size = 10
                    output_directory = 'Images/Uline/thumbnails/'
                    input_path = os.path.join(input_directory, file_name + '.jpg')
                    output_path = os.path.join(output_directory, file_name + '_thumb.jpg')
                    resize_and_pad(input_path, output_path, target_size, frame_size)
                    print("Thumbnail 160*160 saved")

                    """CSV record saving"""
                    row = [
                        'ADD',
                        '9X4Y0',
                        'MARKETPLACE_9X4Y0',
                        model_no,
                        'T',
                        file_name + '_thumb.jpg',
                    ]
                    writer.writerow(row)

                    print(f'Data has been written to CSV')
                    collection.update_one({'_id': record['_id']}, {'$set': {"photo_download_state": True}})
            else:
                print("Could not downloaded")
            print("**********************************")
    except Exception as e:
        pass
client.close()
