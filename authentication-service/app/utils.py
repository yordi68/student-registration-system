import jwt
from flask import request, jsonify, current_app

def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        
        try:
            jwt_secret = current_app.config['JWT_SECRET_KEY']
            jwt_algorithm = current_app.config['JWT_ALGORITHM']
            data = jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])
            request.user = data  # Attach decoded token data to the request
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper
