from flask import Flask
from flask_pymongo import PyMongo
import os
from pymongo import MongoClient
from pymongo.collection import Collection

mongo = PyMongo()  # Flask-PyMongo for basic integration

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('app.config.Config')
    
    # Initialize Flask-PyMongo (if required for some routes)
    mongo.init_app(app)
    
    # Create MongoDB client
    mongo_client = MongoClient(app.config['MONGO_URI'])
    
    # Access the specific database and collection
    db = mongo_client.get_database('authentication-db')
    auth_collection = Collection(db, 'auth')
    
    # Attach to the app for use in routes
    app.mongo_client = mongo_client
    app.db = db
    app.auth_collection = auth_collection
    
    # Register Blueprints
    from .routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    
    return app
