



from pymongo import MongoClient

client = MongoClient("mongodb://admin:admin@localhost:27017")
db = client["randomNumber_db"]
collection = db["randomNumber_data"]

for doc in collection.find():
    print(doc)
    
