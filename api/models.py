from pymongo import MongoClient

client  = MongoClient('mongodb://localhost:27017/')
db = client['task_manager']

task_collection = db['tasks']