



from pymongo import MongoClient

client = MongoClient("mongodb://admin:admin@localhost:27017")
db = client["ESP_NumberDB"]
collection = db["NumberCol"]

for doc in collection.find():
    print(doc)

