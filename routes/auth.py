# Anthony - Updated for SQLAlchemy

# Import Flask components for authentication routes
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# Import datetime for timestamp handling
from datetime import datetime
# Import User and Category models for database operations
from database.models import User, Category
# Import login decorator for protected routes
from decorators import login_required
# Import database utility functions
from database.utils import create_user, authenticate_user, get_user_by_username, create_category

# Create authentication blueprint for organizing routes
auth_bp = Blueprint('auth', __name__)

# Route: /login - Shows login form (GET) or processes login (POST), redirects to dashboard
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login functionality.
    
    This route processes both GET and POST requests for user authentication.
    GET requests display the login form, while POST requests validate
    user credentials and create a session if authentication is successful.
    Admin users are redirected to the admin dashboard, while regular users
    go to the main dashboard.
    
    Returns:
        str: Rendered login template or redirect response
    """
    # Handle POST request for login form submission
    if request.method == 'POST':
        # Get username and password from form data
        username = request.form['username']
        password = request.form['password']

        # Authenticate user with provided credentials
        user = authenticate_user(username, password)

        # If authentication successful, create session
        if user:
            # Store user ID and username in session
            session['user_id'] = user.id
            session['username'] = user.username
            # Show success message to user
            flash('Logged in successfully!', 'success')
            
            # Redirect admin users to admin dashboard, others to regular dashboard
            if username == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            # Show error message for invalid credentials
            flash('Invalid username or password.', 'danger')
    # Render login template for GET requests
    return render_template('login.html')

# Route: /register - Shows registration form (GET) or creates new user (POST), redirects to login
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    
    """
    Handles user registration functionality.
    
    This route processes both GET and POST requests for user registration.
    GET requests display the registration form, while POST requests validate
    form data, check for existing usernames, create a new user account,
    and set up default categories for the new user.
    
    Returns:
        str: Rendered registration template or redirect response
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
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        # Check if username already exists in database
        if get_user_by_username(username):
            flash('Username already exists.', 'danger')
            return render_template('register.html')

        # Create new user account in database
        new_user = create_user(username, email, password)
        
        if not new_user:
            flash('Error creating user account.', 'danger')
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
    
    This route clears the user's session data and redirects them to the
    login page. It requires the user to be logged in (protected by
    @login_required decorator). Also clears dark mode preference from localStorage.
    
    Returns:
        str: Redirect response to login page with script to clear dark mode
    """
    # Remove user data from session
    session.pop('user_id', None)
    session.pop('username', None)
    # Show logout message to user
    flash('You have been logged out.', 'info')
    
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