from pymongo import MongoClient

# MongoDB connection information
mongo_uri = 'mongodb://localhost:27017/'  # Replace with your MongoDB URI
database_name = 'joe'  # Name of your database
new_collection_name = 'bhphotovideo_data'  # Name of the new collection

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]

# Define the three collections
collections = ['TV', 'hard_drives', 'monitors_bh']

# Initialize the new collection
new_collection = db[new_collection_name]

# Loop through each collection and insert documents into new_collection
for collection_name in collections:
    collection = db[collection_name]
    for document in collection.find():
        new_collection.insert_one(document)

print(f"Combined data from {', '.join(collections)} into {new_collection_name} collection.")

# Close the MongoDB connection
client.close()
