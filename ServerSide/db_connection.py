import pymongo
import pymongo.mongo_client

url='localhost:27017'

client=pymongo.MongoClient(url)

db=client['Server']