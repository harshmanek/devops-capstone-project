import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def _parse_port(env_name: str, default: int) -> int:
    val = os.getenv(env_name)
    if not val:
        return default
    # handle values like "tcp://IP:PORT" or plain "5001"
    m = re.search(r'(\d+)$', str(val))
    if m:
        try:
            return int(m.group(1))
        except ValueError:
            pass
    try:
        return int(val)
    except (TypeError, ValueError):
        return default

class Config:
    """Base configuration for User Service"""
    # Database configuration
    SQLALCHEMY_DATABASE_URI = (
    os.getenv('SQLALCHEMY_DATABASE_URI')
    or os.getenv('DATABASE_URL')
    or os.getenv('DATABASE_URI')
    or 'mysql+pymysql://devops_user:devops_password_123@mysql:3306/microservices_db'
)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask configuration
    JSON_SORT_KEYS = False
    
    # Service info
    SERVICE_NAME = 'User Service'
    SERVICE_PORT = _parse_port('USER_SERVICE_PORT', 5001)
