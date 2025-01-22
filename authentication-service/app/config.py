import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://yordanosdev1:VhQWtPoLNC3rq5jX@cluster0.2h58v.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0/authentication-db")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
