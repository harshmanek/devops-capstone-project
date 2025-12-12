import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration for User Service"""
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://devops_user:devops_password_123@localhost:3306/microservices_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask configuration
    JSON_SORT_KEYS = False
    
    # Service info
    SERVICE_NAME = 'User Service'
    SERVICE_PORT = int(os.getenv('USER_SERVICE_PORT', 5001))
