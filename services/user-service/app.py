from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import hashlib

# Import configuration and models
from config import Config
from models import db, User

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database with Flask app
db.init_app(app)

# Create database tables (if they don't exist)
with app.app_context():
    db.create_all()

# ============================================================================
# SECURITY: PASSWORD HASHING
# ============================================================================

def hash_password(password):
    """
    Hash password using SHA-256.
    
    Why hash passwords?
    - If database is compromised, attackers can't read passwords
    - We store hash, not actual password
    - To verify: hash user's input and compare with stored hash
    
    Note: In production, use bcrypt or argon2 (more secure)
    """
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify password by comparing hashes"""
    return hash_password(password) == password_hash

# ============================================================================
# REST API ENDPOINTS
# ============================================================================

# 1. HEALTH CHECK ENDPOINT
@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    Used by Docker/Kubernetes to verify service is running.
    
    Returns:
    - 200 OK if service is healthy
    - Status information
    """
    return jsonify({
        'status': 'healthy',
        'service': 'User Service',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# ============================================================================

# 2. CREATE USER (REGISTER)
@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user (registration endpoint).
    
    Request body:
    {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "secure_password_123"
    }
    
    Response:
    - 201 Created: User created successfully
    - 400 Bad Request: Missing fields or validation error
    - 409 Conflict: Username or email already exists
    """
    try:
        # Get JSON data from request body
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({
                'error': 'Missing required fields: username, email, password'
            }), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Validate input
        if len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email address'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            return jsonify({
                'error': 'Username or email already exists'
            }), 409
        
        # Create new user
        user = User(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            password_hash=hash_password(password)
        )
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Error creating user: {str(e)}'
        }), 500

# ============================================================================

# 3. GET ALL USERS
@app.route('/users', methods=['GET'])
def get_all_users():
    """
    Get all users (with pagination).
    
    Query parameters:
    - page: Page number (default: 1)
    - per_page: Users per page (default: 10)
    
    Response:
    - 200 OK: List of users
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Query with pagination
        paginated_users = User.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'total': paginated_users.total,
            'pages': paginated_users.pages,
            'current_page': page,
            'per_page': per_page,
            'users': [user.to_dict() for user in paginated_users.items]
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error fetching users: {str(e)}'}), 500

# ============================================================================

# 4. GET USER BY ID
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a specific user by ID.
    
    URL parameter:
    - user_id: User's UUID
    
    Response:
    - 200 OK: User details
    - 404 Not Found: User doesn't exist
    """
    try:
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': f'Error fetching user: {str(e)}'}), 500

# ============================================================================

# 5. UPDATE USER
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update user information.
    
    Request body (all optional):
    {
        "username": "new_username",
        "email": "newemail@example.com"
    }
    
    Response:
    - 200 OK: User updated
    - 404 Not Found: User doesn't exist
    - 409 Conflict: Username/email already taken
    """
    try:
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update username if provided
        if 'username' in data:
            new_username = data['username'].strip()
            if len(new_username) < 3:
                return jsonify({'error': 'Username must be at least 3 characters'}), 400
            
            # Check if new username is already taken
            existing = User.query.filter_by(username=new_username).first()
            if existing and existing.id != user_id:
                return jsonify({'error': 'Username already taken'}), 409
            
            user.username = new_username
        
        # Update email if provided
        if 'email' in data:
            new_email = data['email'].strip()
            if '@' not in new_email or '.' not in new_email:
                return jsonify({'error': 'Invalid email'}), 400
            
            # Check if new email is already taken
            existing = User.query.filter_by(email=new_email).first()
            if existing and existing.id != user_id:
                return jsonify({'error': 'Email already taken'}), 409
            
            user.email = new_email
        
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating user: {str(e)}'}), 500

# ============================================================================

# 6. DELETE USER
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user.
    
    Response:
    - 200 OK: User deleted
    - 404 Not Found: User doesn't exist
    """
    try:
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting user: {str(e)}'}), 500

# ============================================================================

# 7. LOGIN ENDPOINT
@app.route('/login', methods=['POST'])
def login():
    """
    Login endpoint (authentication).
    
    Request body:
    {
        "email": "john@example.com",
        "password": "secure_password_123"
    }
    
    Response:
    - 200 OK: Login successful with user info
    - 401 Unauthorized: Invalid credentials
    """
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['email', 'password']):
            return jsonify({'error': 'Missing email or password'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Verify password
        if not user or not verify_password(password, user.password_hash):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error during login: {str(e)}'}), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    print(f"Starting User Service on port {Config.SERVICE_PORT}...")
    print(f"Database: {Config.SQLALCHEMY_DATABASE_URI}")
    print(f"Endpoints available:")
    print(f"  GET  /health")
    print(f"  POST /users (create user)")
    print(f"  GET  /users (list all)")
    print(f"  GET  /users/<id> (get user)")
    print(f"  PUT  /users/<id> (update user)")
    print(f"  DELETE /users/<id> (delete user)")
    print(f"  POST /login")
    
    # Run Flask development server
    app.run(
        host='0.0.0.0',  # Listen on all interfaces
        port=Config.SERVICE_PORT,
        debug=True  # Enable auto-reload on code changes
    )
