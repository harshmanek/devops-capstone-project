"""
Order Service - Configuration
Database and application settings
"""

import os

class Config:
    """
    Order Service Configuration
    """
    
    # Flask Settings
    DEBUG = True
    TESTING = False
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = (
        os.getenv('SQLALCHEMY_DATABASE_URI') 
        or os.getenv('DATABASE_URL') 
        or os.getenv('DATABASE_URI') 
        or 'mysql+pymysql://devops_user:devops_password_123@mysql:3306/microservices_db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Log SQL queries
    
    # Connection Pool Settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 20,
    }
    
    # Service URLs
    USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://user-service:5001')
    PRODUCT_SERVICE_URL = os.getenv('PRODUCT_SERVICE_URL', 'http://product-service:5002')
    
    # Request Timeout
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT',5))  # seconds
    SERVICE_PORT = int(os.getenv('SERVICE_PORT', 5003))
    # CORS Settings
    CORS_HEADERS = 'Content-Type'

class DevelopmentConfig(Config):
    """Development Configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production Configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing Configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
