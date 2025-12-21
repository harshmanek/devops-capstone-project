"""
Order Service - SQLAlchemy Models
Database models for order management
"""

from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime

db = SQLAlchemy()

class Order(db.Model):
    """
    Order Model - Represents an order in the system
    
    Attributes:
        id: UUID primary key (36 chars)
        user_id: UUID of the user who placed the order
        product_id: UUID of the ordered product
        quantity: Number of units ordered
        total_price: Total order amount (price × quantity)
        status: Order status (pending, confirmed, shipped, delivered, cancelled)
        created_at: Timestamp when order was created
        updated_at: Timestamp when order was last updated
    """
    
    __tablename__ = 'orders'
    
    # Primary Key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    
    # Foreign Keys (References to other services)
    user_id = db.Column(db.String(36), nullable=False, index=True)
    product_id = db.Column(db.String(36), nullable=False, index=True)
    
    # Order Information
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Order Status
    status = db.Column(
        db.Enum('pending', 'confirmed', 'shipped', 'delivered', 'cancelled'),
        default='pending',
        nullable=False,
        index=True
    )
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                          onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        """String representation of Order"""
        return f'<Order {self.id}: User={self.user_id}, Product={self.product_id}, Status={self.status}>'
    
    def to_dict(self):
        """Convert order to dictionary (for JSON responses)"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'total_price': float(self.total_price),
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
