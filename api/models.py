from pymongo import MongoClient
import os

mongo_url = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongo_url)

db_name = os.environ.get('DB_NAME', 'taskdb')
db = client[db_name]
task_collection = db['tasks']