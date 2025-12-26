"""
Order Service - Flask REST API
Manages order processing and service integration
Port: 5003

This service communicates with:
- User Service (http://localhost:5001) - User validation
- Product Service (http://localhost:5002) - Product & stock management
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import requests
import os
from config import Config
from models import db, Order

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)
CORS(app)

# Create database tables
with app.app_context():
    db.create_all()

# ==================== SERVICE ENDPOINTS ====================

# Replace hardcoded URLs with Config values
USER_SERVICE_URL = Config.USER_SERVICE_URL
PRODUCT_SERVICE_URL = Config.PRODUCT_SERVICE_URL

# ==================== HELPER FUNCTIONS ====================

def validate_user(user_id):
    """
    Validate if user exists in User Service
    
    Args:
        user_id: UUID of the user
    
    Returns:
        dict: User data if valid, None if not found
    """
    try:
        response = requests.get(f"{USER_SERVICE_URL}/users/{user_id}", timeout=Config.REQUEST_TIMEOUT)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error validating user: {str(e)}")
        return None

def validate_product(product_id):
    """
    Validate if product exists in Product Service
    
    Args:
        product_id: UUID of the product
    
    Returns:
        dict: Product data if valid, None if not found
    """
    try:
        response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}", timeout=Config.REQUEST_TIMEOUT)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error validating product: {str(e)}")
        return None

def reduce_product_stock(product_id, quantity):
    """
    Reduce product stock in Product Service
    
    Args:
        product_id: UUID of the product
        quantity: Number of units to reduce
    
    Returns:
        bool: True if successful, False if failed
    """
    try:
        response = requests.patch(
            f"{PRODUCT_SERVICE_URL}/products/{product_id}/stock",
            json={"quantity_change": -quantity},
            timeout=Config.REQUEST_TIMEOUT
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error reducing stock: {str(e)}")
        return False

def restore_product_stock(product_id, quantity):
    """
    Restore product stock in Product Service (for cancelled orders)
    
    Args:
        product_id: UUID of the product
        quantity: Number of units to restore
    
    Returns:
        bool: True if successful, False if failed
    """
    try:
        response = requests.patch(
            f"{PRODUCT_SERVICE_URL}/products/{product_id}/stock",
            json={"quantity_change": quantity},
            timeout=Config.REQUEST_TIMEOUT
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error restoring stock: {str(e)}")
        return False

# ==================== HEALTH CHECK ====================

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    Returns service status and timestamp
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Order Service',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# ==================== CREATE ORDER ====================

@app.route('/orders', methods=['POST'])
def create_order():
    """
    Create a new order
    
    Request body:
    {
        "user_id": "user-uuid",
        "product_id": "product-uuid",
        "quantity": 2
    }
    
    Process:
    1. Validate user exists
    2. Validate product exists
    3. Check product stock
    4. Create order in database
    5. Reduce product stock
    
    Returns:
    201: Order created successfully
    400: Validation error
    404: User or product not found
    500: Server error
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'Request body is empty'}), 400
        
        if not data.get('user_id'):
            return jsonify({'error': 'user_id is required'}), 400
        
        if not data.get('product_id'):
            return jsonify({'error': 'product_id is required'}), 400
        
        if not data.get('quantity'):
            return jsonify({'error': 'quantity is required'}), 400
        
        # Validate quantity
        try:
            quantity = int(data.get('quantity'))
            if quantity <= 0:
                return jsonify({'error': 'Quantity must be greater than 0'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Quantity must be an integer'}), 400
        
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        
        # ========== STEP 1: Validate User ==========
        user = validate_user(user_id)
        if not user:
            return jsonify({
                'error': f'User not found',
                'user_id': user_id
            }), 404
        
        # ========== STEP 2: Validate Product ==========
        product = validate_product(product_id)
        if not product:
            return jsonify({
                'error': f'Product not found',
                'product_id': product_id
            }), 404
        
        # ========== STEP 3: Check Stock ==========
        product_stock = product.get('stock_quantity', 0)
        if product_stock < quantity:
            return jsonify({
                'error': f'Insufficient stock',
                'available': product_stock,
                'requested': quantity
            }), 400
        
        # ========== STEP 4: Calculate Total Price ==========
        product_price = float(product.get('price', 0))
        total_price = product_price * quantity
        
        # ========== STEP 5: Create Order ==========
        order = Order(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            total_price=total_price,
            status='pending'
        )
        
        db.session.add(order)
        db.session.commit()
        
        # ========== STEP 6: Reduce Stock ==========
        stock_reduced = reduce_product_stock(product_id, quantity)
        if not stock_reduced:
            # Rollback order if stock reduction fails
            db.session.delete(order)
            db.session.commit()
            return jsonify({
                'error': 'Failed to reduce product stock'
            }), 500
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict(),
            'user': user,
            'product': product
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error creating order: {str(e)}'}), 500

# ==================== GET ALL ORDERS ====================

@app.route('/orders', methods=['GET'])
def get_all_orders():
    """
    Get all orders with pagination
    
    Query parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 10)
    - status: Filter by status (optional)
    
    Returns:
    200: List of orders
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', None, type=str)
        
        # Build query
        query = Order.query
        if status:
            query = query.filter_by(status=status)
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        orders = [order.to_dict() for order in pagination.items]
        
        return jsonify({
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page,
            'orders': orders
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error fetching orders: {str(e)}'}), 500

# ==================== GET SPECIFIC ORDER ====================

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """
    Get a specific order by ID
    
    Parameters:
    - order_id: UUID of the order
    
    Returns:
    200: Order details
    404: Order not found
    """
    try:
        order = Order.query.filter_by(id=order_id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify(order.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': f'Error fetching order: {str(e)}'}), 500

# ==================== GET ORDERS BY USER ====================

@app.route('/orders/user/<user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    """
    Get all orders for a specific user
    
    Parameters:
    - user_id: UUID of the user
    
    Returns:
    200: List of user's orders
    404: User not found
    """
    try:
        # Validate user exists
        user = validate_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        pagination = Order.query.filter_by(user_id=user_id).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        orders = [order.to_dict() for order in pagination.items]
        
        return jsonify({
            'user_id': user_id,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page,
            'orders': orders
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error fetching orders: {str(e)}'}), 500

# ==================== UPDATE ORDER STATUS ====================

@app.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    """
    Update order status
    
    Parameters:
    - order_id: UUID of the order
    
    Request body:
    {
        "status": "confirmed"  # pending, confirmed, shipped, delivered, cancelled
    }
    
    Returns:
    200: Order updated successfully
    404: Order not found
    400: Invalid status
    500: Server error
    """
    try:
        # Find order
        order = Order.query.filter_by(id=order_id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Get JSON data
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({'error': 'status field is required'}), 400
        
        new_status = data.get('status')
        valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
        
        if new_status not in valid_statuses:
            return jsonify({
                'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
            }), 400
        
        # If cancelling, restore stock
        if new_status == 'cancelled' and order.status != 'cancelled':
            stock_restored = restore_product_stock(order.product_id, order.quantity)
            if not stock_restored:
                return jsonify({
                    'error': 'Failed to restore product stock'
                }), 500
        
        # Update status
        order.status = new_status
        db.session.commit()
        
        return jsonify({
            'message': 'Order updated successfully',
            'order': order.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating order: {str(e)}'}), 500

# ==================== CONFIRM ORDER ====================

@app.route('/orders/<order_id>/confirm', methods=['POST'])
def confirm_order(order_id):
    """
    Confirm an order (change status from pending to confirmed)
    
    Parameters:
    - order_id: UUID of the order
    
    Returns:
    200: Order confirmed successfully
    404: Order not found
    400: Order already confirmed/cancelled
    500: Server error
    """
    try:
        order = Order.query.filter_by(id=order_id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        if order.status != 'pending':
            return jsonify({
                'error': f'Cannot confirm order with status: {order.status}'
            }), 400
        
        order.status = 'confirmed'
        db.session.commit()
        
        return jsonify({
            'message': 'Order confirmed successfully',
            'order': order.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error confirming order: {str(e)}'}), 500

# ==================== DELETE ORDER ====================

@app.route('/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    """
    Delete an order (only pending orders can be deleted)
    
    Parameters:
    - order_id: UUID of the order
    
    Returns:
    200: Order deleted successfully
    404: Order not found
    400: Cannot delete confirmed/shipped order
    500: Server error
    """
    try:
        order = Order.query.filter_by(id=order_id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        if order.status not in ['pending', 'cancelled']:
            return jsonify({
                'error': f'Cannot delete order with status: {order.status}'
            }), 400
        
        # Restore stock if not already cancelled
        if order.status == 'pending':
            restore_product_stock(order.product_id, order.quantity)
        
        db.session.delete(order)
        db.session.commit()
        
        return jsonify({'message': 'Order deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting order: {str(e)}'}), 500

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
    # Bind to 0.0.0.0 so the service is reachable from other containers/host
    app.run(host='0.0.0.0', port=Config.SERVICE_PORT, debug=True)
