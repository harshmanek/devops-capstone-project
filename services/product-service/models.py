from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4

db = SQLAlchemy()

class Product(db.Model):
    """
    Product model represents the 'products' table in MySQL.
    
    Attributes:
    - id: UUID primary key
    - name: Product name (indexed for search)
    - description: Product details
    - price: Product price (stored as DECIMAL for accuracy)
    stock_quantity: Available inventory (indexed for stocck checks)
    - created_at: Creation timestamp
    - updated_at: Last update timestamp
    """
    
    __tablename__ = 'products'
    
    
    id = db.Column(
            db.String(36),
            primary_key=True,
            default=lambda: str(uuid4()),
            nullable=False
     )
    name = db.Column(
            db.String(255),
            nullable=False,
            index=True
     )
    description = db.Column(
            db.Text,
            nullable=True
     )
    price = db.Column(
            db.Numeric(10,2),
            nullable=True
     )
    stock_quantity = db.Column(
            db.Integer,
            default=0,
            nullable=False,
            index=True
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
        return f'<Product {self.name}>'

    def to_dict(self):
        """"Convert Product object to dictionary"""
        return {
            'id':self.id,
            'name':self.name,
            'description':self.description,
            'price':float(self.price),
            'stock_quantity':self.stock_quantity,
            'created_at':self.created_at.isoformat(),
            'updated_at':self.updated_at.isoformat()
        }









