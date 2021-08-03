import os
from pymongo import MongoClient

ATLAS_CONNECTION_STRING = f"mongodb+srv://admin:{os.environ.get('MONGO_PASSWORD')}@cluster0.bol4s.mongodb.net/{os.environ.get('MONGO_DB_NAME')}?retryWrites=true&w=majority"
EC2_CONNECTION_STRING = f"mongodb://statsUser:{os.environ.get('MONGO_PASSWORD')}@18.118.15.158/{os.environ.get('MONGO_DB_NAME')}"
client = MongoClient(EC2_CONNECTION_STRING)
db = client[os.environ.get("MONGO_DB_NAME")]