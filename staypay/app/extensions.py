from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Initialize the plugins but don't bind them to the app yet
db = SQLAlchemy()
jwt = JWTManager()