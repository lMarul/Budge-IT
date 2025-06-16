# Anthony - Updated for SQLAlchemy

# Import wraps for preserving function metadata
from functools import wraps
# Import Flask session, redirect, url_for, and flash for authentication
from flask import session, redirect, url_for, flash
# Import SQLAlchemy models
from .models import User

def login_required(f):
    """
    Decorator to require user login for protected routes.
    
    This decorator checks if a user is logged in by looking for 'user_id'
    in the session. If not logged in, it redirects to the login page
    with an appropriate error message.
    
    Args:
        f: The function to be decorated (route handler)
    
    Returns:
        function: Decorated function that checks login status
    """
    # Preserve original function metadata
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in by looking for user_id in session
        if 'user_id' not in session:
            # Show error message and redirect to login page
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        # Execute original function if user is logged in
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator to require admin privileges for protected routes.
    
    This decorator first checks if a user is logged in, then verifies
    that the user has admin privileges by checking if their username
    is 'admin'. If either check fails, it redirects appropriately.
    
    Args:
        f: The function to be decorated (route handler)
    
    Returns:
        function: Decorated function that checks admin status
    """
    # Preserve original function metadata
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in first
        if 'user_id' not in session:
            # Show error message and redirect to login page
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Get current user from database using SQLAlchemy
        user = User.query.get(session['user_id'])
        # Check if user exists and has admin username
        if not user or user.username != 'admin':
            # Show access denied message and redirect to dashboard
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('main.dashboard'))
        # Execute original function if user is admin
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """
    Gets the current user data from the session.
    
    This function retrieves the current user's information from the database
    based on the user_id stored in the session. It returns None if no user
    is logged in or if the user is not found.
    
    Returns:
        User or None: Current user object or None if not logged in
    """
    # Return None if user is not logged in
    if 'user_id' not in session:
        return None
    
    # Get current user from database using SQLAlchemy
    return User.query.get(session['user_id'])

def is_admin():
    """
    Checks if the current user has admin privileges.
    
    This function determines if the currently logged-in user has admin
    privileges by checking if their username is 'admin'.
    
    Returns:
        bool: True if current user is admin, False otherwise
    """
    # Get current user data
    user = get_current_user()
    # Return True if user exists and has admin username
    return user and user.username == 'admin' 