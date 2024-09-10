import csv
import os

from pymongo import MongoClient


def list_jpeg_files(directory):
    jpeg_files = [f for f in os.listdir(directory) if f.endswith('.jpg') or f.endswith('.jpeg')]
    return jpeg_files

i=1

mongo_uri = 'mongodb://localhost:27017/'
database_name = 'Uline'
collection_name = 'Products'

client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

if __name__ == "__main__":
    directory_path = 'Images/Uline/output_uline'  # Replace with your directory path

    jpeg_files = list_jpeg_files(directory_path)

    with open('Images/uline_registery.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='^')
        for row in csv_reader:
            if row[-1] not in jpeg_files:
                print(row[3])
                i+=1
    print(i)