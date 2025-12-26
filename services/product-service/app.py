"""
Product Service - Flask REST API
Manages product catalog and inventory
Port: 5002
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from config import Config
from models import db, Product

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)
CORS(app)

# Create database tables
with app.app_context():
    db.create_all()

# ==================== HEALTH CHECK ====================

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    Returns service status and timestamp
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Product Service',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# ==================== CREATE PRODUCT ====================

@app.route('/products', methods=['POST'])
def create_product():
    """
    Create a new product
    
    Request body:
    {
        "name": "Product Name",
        "description": "Product description",
        "price": 99.99,
        "stock_quantity": 50
    }
    
    Returns:
    201: Product created successfully
    400: Validation error
    500: Server error
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'Request body is empty'}), 400
        
        if not data.get('name'):
            return jsonify({'error': 'Product name is required'}), 400
        
        if not data.get('price'):
            return jsonify({'error': 'Product price is required'}), 400
        
        # Validate name length
        if len(data.get('name', '')) < 3:
            return jsonify({'error': 'Product name must be at least 3 characters'}), 400
        
        # Validate price is positive
        try:
            price = float(data.get('price'))
            if price <= 0:
                return jsonify({'error': 'Product price must be greater than 0'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Product price must be a valid number'}), 400
        
        # Create new product
        product = Product(
            name=data.get('name'),
            description=data.get('description', ''),
            price=price,
            stock_quantity=int(data.get('stock_quantity', 0))
        )
        
        # Add to database
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error creating product: {str(e)}'}), 500

# ==================== GET ALL PRODUCTS ====================

@app.route('/products', methods=['GET'])
def get_all_products():
    """
    Get all products with pagination
    
    Query parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 10)
    
    Returns:
    200: List of products
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Query products with pagination
        pagination = Product.query.paginate(page=page, per_page=per_page, error_out=False)
        
        products = [product.to_dict() for product in pagination.items]
        
        return jsonify({
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page,
            'products': products
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error fetching products: {str(e)}'}), 500

# ==================== GET SPECIFIC PRODUCT ====================

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """
    Get a specific product by ID
    
    Parameters:
    - product_id: UUID of the product
    
    Returns:
    200: Product details
    404: Product not found
    """
    try:
        product = Product.query.filter_by(id=product_id).first()
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify(product.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': f'Error fetching product: {str(e)}'}), 500

# ==================== UPDATE PRODUCT ====================

@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Update a product
    
    Parameters:
    - product_id: UUID of the product
    
    Request body (all fields optional):
    {
        "name": "Updated name",
        "description": "Updated description",
        "price": 199.99,
        "stock_quantity": 100
    }
    
    Returns:
    200: Product updated successfully
    404: Product not found
    400: Validation error
    500: Server error
    """
    try:
        # Find product
        product = Product.query.filter_by(id=product_id).first()
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is empty'}), 400
        
        # Update fields if provided
        if 'name' in data:
            if len(data['name']) < 3:
                return jsonify({'error': 'Product name must be at least 3 characters'}), 400
            product.name = data['name']
        
        if 'description' in data:
            product.description = data['description']
        
        if 'price' in data:
            try:
                price = float(data['price'])
                if price <= 0:
                    return jsonify({'error': 'Product price must be greater than 0'}), 400
                product.price = price
            except (ValueError, TypeError):
                return jsonify({'error': 'Product price must be a valid number'}), 400
        
        if 'stock_quantity' in data:
            product.stock_quantity = int(data['stock_quantity'])
        
        # Commit changes
        db.session.commit()
        
        return jsonify({
            'message': 'Product updated successfully',
            'product': product.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating product: {str(e)}'}), 500

# ==================== UPDATE STOCK ====================

@app.route('/products/<product_id>/stock', methods=['PATCH'])
def update_stock(product_id):
    """
    Update product stock quantity
    
    Parameters:
    - product_id: UUID of the product
    
    Request body:
    {
        "quantity_change": -5  # Negative to decrease, positive to increase
    }
    
    Returns:
    200: Stock updated successfully
    404: Product not found
    400: Validation error
    500: Server error
    """
    try:
        # Find product
        product = Product.query.filter_by(id=product_id).first()
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Get JSON data
        data = request.get_json()
        
        if not data or 'quantity_change' not in data:
            return jsonify({'error': 'quantity_change field is required'}), 400
        
        # Get quantity change
        try:
            quantity_change = int(data['quantity_change'])
        except (ValueError, TypeError):
            return jsonify({'error': 'quantity_change must be an integer'}), 400
        
        # Check if stock will go negative
        new_quantity = product.stock_quantity + quantity_change
        if new_quantity < 0:
            return jsonify({
                'error': f'Insufficient stock. Current: {product.stock_quantity}, Requested: {abs(quantity_change)}'
            }), 400
        
        # Update stock
        product.stock_quantity = new_quantity
        db.session.commit()
        
        return jsonify({
            'message': 'Stock updated successfully',
            'product': product.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating stock: {str(e)}'}), 500

# ==================== DELETE PRODUCT ====================

@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    Delete a product
    
    Parameters:
    - product_id: UUID of the product
    
    Returns:
    200: Product deleted successfully
    404: Product not found
    500: Server error
    """
    try:
        # Find product
        product = Product.query.filter_by(id=product_id).first()
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Delete product
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Product deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting product: {str(e)}'}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

# ==================== RUN SERVER ====================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.SERVICE_PORT, debug=True)
