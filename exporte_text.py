from pymongo import MongoClient
import csv
import re


def clean_value(value):
    """Convert value to string, replace None with empty string, and remove quotes."""
    if value is None:
        return ''
    value = str(value)
    value = re.sub(r"[\"\'\^\|\-\_]", " ", value)
    return value.replace('\n','')

mongo_uri = 'mongodb://localhost:27017/'
database_name = 'Uline'
collection_name = 'Products'

client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# Specify the output file
output_file = 'Exports/uline_output.csv'

# Fetch records from the MongoDB collection
records = collection.find()
# header_text = 'Item Master Primary Spec/Common Information/Universal Product Code ^	Item Master Primary Spec/Common Information/Master Requirement Code ^ Item Master Primary Spec/Common Information/Product name ^ Item Master Primary Spec/Sale Pricing/Sale Price ^ Item Master Primary Spec/Sale Pricing/Sale Price Unit ^ Item Master Primary Spec/Common Information/Weight ^ Item Master Primary Spec/Common Information/Original Equipment Manufacturer Name ^ Item Master Primary Spec/Long Description ^ Item Master Primary Spec/Common Information/Original Equipment Manufacturer Part Number'
header_text = 'Item Master Primary Spec/Common Information/Product Model Number ^ Item Master Primary Spec/Common Information/Product name ^ Item Master Primary Spec/Sale Pricing/Sale Price ^ Item Master Primary Spec/Common Information/Weight ^ Item Master Primary Spec/Long Description '
# Open the output file in write mode
with open(output_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='^', quoting=csv.QUOTE_MINIMAL)
    file.write(header_text + '\n')
    for record in records:
        row = [
            clean_value(record.get('model_no', '')),
            clean_value(record.get('title', '')),
            clean_value(record.get('price', ''))+' $',
            clean_value(record.get('weight', ''))+' lb',
            clean_value(record.get('description', '')),
        ]
        writer.writerow(row)

print(f'Data has been written to {output_file}')



