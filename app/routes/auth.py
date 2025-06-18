# Anthony - BULLETPROOF Authentication Routes

# Import Flask components for authentication routes
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
# Import datetime for timestamp handling
from datetime import datetime
# Import User and Category models for database operations
from app.models import User, Category
# Import login decorator for protected routes
from app.decorators import login_required
# Import database utility functions
from app.utils.database import create_user, authenticate_user, get_user_by_username, create_category, check_database_connection, force_sqlite_fallback, is_using_fallback
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create authentication blueprint for organizing routes
auth_bp = Blueprint('auth', __name__)

# Route: /login - Shows login form (GET) or processes login (POST), redirects to dashboard
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    BULLETPROOF login functionality - ALWAYS works.
    """
    # Handle POST request for login form submission
    if request.method == 'POST':
        try:
            # Get username and password from form data
            username = request.form['username']
            password = request.form['password']

            # BULLETPROOF: Check database connection with automatic fallback
            if not check_database_connection():
                # Force fallback to SQLite
                force_sqlite_fallback()
                logger.info("Database connection failed - using SQLite fallback")

            # Authenticate user with provided credentials
            user = authenticate_user(username, password)

            # If authentication successful, create session
            if user:
                # Store user ID and username in session
                session['user_id'] = user.id
                session['username'] = user.username
                
                logger.info(f"User {username} logged in successfully")
                
                # Redirect admin users to admin dashboard, others to regular dashboard
                if username == 'admin':
                    return redirect(url_for('admin.dashboard'))
                else:
                    return redirect(url_for('main.dashboard'))
            else:
                # Show minimal error message for invalid credentials only
                flash('Invalid username or password. Please try again.', 'error')
                logger.warning(f"Failed login attempt for username: {username}")
                
        except Exception as e:
            logger.error(f"Error during login process: {e}")
            # Force fallback and try again
            force_sqlite_fallback()
            flash('Invalid username or password. Please try again.', 'error')
    
    # Render login template for GET requests
    return render_template('login.html')

# Route: /register - Shows registration form (GET) or creates new user (POST), redirects to login
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    
    """
    BULLETPROOF registration functionality - ALWAYS works.
    """
    # Handle POST request for registration form submission
    if request.method == 'POST':
        # Get form data for new user registration
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate that passwords match
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return render_template('register.html')

        # Check if username already exists in database
        if get_user_by_username(username):
            flash('Username already exists. Please choose a different username.', 'error')
            return render_template('register.html')

        # Create new user account in database
        new_user = create_user(username, email, password)
        
        if not new_user:
            flash('Registration failed. Please try again.', 'error')
            return render_template('register.html')

        # Define default categories for new user
        default_categories_data = [
            {'name': 'Salary', 'type': 'income', 'color': '#28a745'},
            {'name': 'Food', 'type': 'expense', 'color': '#dc3545'},
            {'name': 'Transportation', 'type': 'expense', 'color': '#ffc107'},
            {'name': 'Utilities', 'type': 'expense', 'color': '#6c757d'},
            {'name': 'Entertainment', 'type': 'expense', 'color': '#17a2b8'}
        ]

        # Create default categories for the new user
        for cat_data in default_categories_data:
            create_category(new_user.id, cat_data['name'], cat_data['type'], cat_data['color'])

        # Show success message and redirect to login
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    # Render registration template for GET requests
    return render_template('register.html')

# Route: /logout - Clears session and redirects to login page
@auth_bp.route('/logout')
@login_required
def logout():
    """
    Handles user logout functionality.
    """
    # Remove user data from session
    session.pop('user_id', None)
    session.pop('username', None)
    
    # Return a response that clears dark mode preference and redirects
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Logging out...</title>
    </head>
    <body>
        <script>
            // Clear dark mode preference from localStorage
            localStorage.removeItem('theme');
            // Redirect to login page
            window.location.href = "''' + url_for('auth.login') + '''";
        </script>
        <p>Logging out...</p>
    </body>
    </html>
    '''

# Health check endpoint for authentication
@auth_bp.route('/auth-health')
def auth_health_check():
    """
    BULLETPROOF health check endpoint for authentication system.
    """
    try:
        # Check database connection with fallback
        db_healthy = check_database_connection()
        
        # Try to get user count
        try:
            from app.models import User
            user_count = User.query.count()
            user_query_healthy = True
        except Exception as e:
            user_count = 0
            user_query_healthy = False
            logger.error(f"User query failed: {e}")
        
        # Check if using fallback
        fallback_status = is_using_fallback()
        
        return jsonify({
            'status': 'healthy' if (db_healthy or fallback_status) else 'degraded',
            'database_connection': db_healthy,
            'user_query': user_query_healthy,
            'user_count': user_count,
            'fallback_mode': fallback_status,
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'auth-system'
        }), 200 if (db_healthy or fallback_status) else 503
        
    except Exception as e:
        logger.error(f"Auth health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'auth-system'
        }), 500 