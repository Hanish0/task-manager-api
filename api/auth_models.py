from api.models import db
from passlib.hash import pbkdf2_sha256

user_collection = db['users']

def create_user(username, password):
    if user_collection.find_one({"username": username}):
        return None
    hashed_password = pbkdf2_sha256.hash(password)

    user = {
        "username": username,
        "password": hashed_password
    }

    user_id = user_collection.insert_one(user).inserted_id
    return str(user_id)

def authenticate_user(username, password):
    user = user_collection.find_one({"username": username})

    if user and pbkdf2_sha256.verify(password, user["password"]):
        return user
    return None