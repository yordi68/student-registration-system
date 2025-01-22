from flask_pymongo import ObjectId

class User:
    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password

    def to_dict(self):
        return {
            "username": self.username,
            "hashed_password": self.hashed_password
        }
