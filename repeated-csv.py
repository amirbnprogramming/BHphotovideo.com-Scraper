import csv
import os


def list_jpeg_files(directory):
    jpeg_files = [f for f in os.listdir(directory) if f.endswith('.jpg') or f.endswith('.jpeg')]
    return jpeg_files
i=1

if __name__ == "__main__":
    directory_path = 'Images/BH/BH'  # Replace with your directory path

    jpeg_files = list_jpeg_files(directory_path)


    with open('Images/bh_registery.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='^')
        for row in csv_reader:
            if row[-1] not in jpeg_files:
                print(row[3])

