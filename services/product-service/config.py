import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration for Product Service"""
    SQLALCHEMY_DATABASE_URI = (
    os.getenv('SQLALCHEMY_DATABASE_URI')
    or os.getenv('DATABASE_URL')
    or os.getenv('DATABASE_URI')
    or 'mysql+pymysql://devops_user:devops_password_123@mysql:3306/microservices_db'
)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SERVICE_NAME = 'Product Service'
    SERVICE_PORT = int(os.getenv('SERVICE_PORT',5002))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT',5))  # seconds
