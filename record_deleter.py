import pymongo

# Connect to MongoDB
mongo_url = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(mongo_url)
db = client['joe']
collection = db['bhphotovideo_data']



# Define the filter to find documents where img_link and price are both null
filter = {
    "img_link": None,
    "price": None
}

# Delete documents matching the filter
result = collection.delete_many(filter)

# Output the number of deleted documents
print(f"Deleted {result.deleted_count} documents where img_link and price are null.")