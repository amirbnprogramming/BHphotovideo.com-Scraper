from pymongo import MongoClient

mongo_uri = 'mongodb://localhost:27017/'  # Replace with your MongoDB URI
database_name = 'joe'  # Name of your database
collection_name = 'bhphotovideo_data'  # Name of the new collection


# Connect to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB connection string
db = client[database_name]

# Define the fields you want to set to null
update_fields = {'weight': None, 'img_link': None}  # Replace with your fields

# Select the collection
collection = db[collection_name]

# Update all documents in the collection
result = collection.update_many({}, {'$set': update_fields})

# Print the result
print(f'Collection: {collection_name}')
print(f'Matched {result.matched_count} documents and modified {result.modified_count} documents.')

# Close the connection
client.close()
