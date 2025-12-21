import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration for Product Service"""
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        'mysql+pymysql://devops_user:devops_password_123@localhost:3306/microservices_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SERVICE_NAME = 'Product Service'
    SERVICE_PORT = int(os.getenv('PRODUCT_SERVICE_PORT',5002))