from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

# Initialize SQLAlchemy (database ORM)
db = SQLAlchemy()

class User(db.Model):
    """
    User model represents the 'users' table in MySQL.
    
    Each attribute corresponds to a column in the database:
    - id: UUID primary key (unique identifier)
    - username: Unique username (cannot have duplicates)
    - email: Unique email address
    - password_hash: Hashed password (never store plain text!)
    - created_at: Automatically set when created
    - updated_at: Automatically updated when modified
    """
    
    __tablename__ = 'users'
    
    # Columns definition
    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False
    )
    username = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )
    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )
    password_hash = db.Column(
        db.String(255),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    def __repr__(self):
        """String representation for debugging"""
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Convert User object to dictionary (JSON-compatible)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
