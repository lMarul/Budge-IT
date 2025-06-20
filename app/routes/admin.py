# Vince - Updated for SQLAlchemy

# Import Flask components for admin routes
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
# Import datetime for date handling
from datetime import datetime
# Import login decorator for protected routes
from app.decorators import login_required, admin_required
# Import models for database operations
from app.models import User, Category, Transaction
# Import JSON for data serialization
import json
# Import save_database utility
from app.utils.database import save_database

# Create admin blueprint for organizing admin routes
admin_bp = Blueprint('admin', __name__)

# Route: /admin - Shows admin dashboard with system statistics
@admin_bp.route('/admin')
@admin_required
def dashboard():
    """
    Displays the admin dashboard with system-wide statistics.
    
    This route provides an overview of the entire system including total
    users, categories, transactions, and financial summaries across all users.
    It requires admin privileges to access.
    
    Returns:
        str: Rendered admin dashboard template with statistics
    """
    try:
        # Get database statistics using SQLAlchemy
        total_users = User.query.count()
        total_categories = Category.query.count()
        total_transactions = Transaction.query.count()
        
        # Calculate total income and expense across all users
        total_income = sum(t.amount for t in Transaction.query.filter_by(transaction_type='income').all())
        total_expense = sum(t.amount for t in Transaction.query.filter_by(transaction_type='expense').all())
        
        # Render admin dashboard with statistics
        return render_template('admin_functions/admin_dashboard.html',
                               total_users=total_users,
                               total_categories=total_categories,
                               total_transactions=total_transactions,
                               total_income=total_income,
                               total_expense=total_expense)
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error in admin dashboard route: {e}")
        
        # Return fallback values if database connection fails
        return render_template('admin_functions/admin_dashboard.html',
                               total_users=0,
                               total_categories=0,
                               total_transactions=0,
                               total_income=0,
                               total_expense=0)

# Route: /admin/users - Shows user management page with all users
@admin_bp.route('/admin/users')
@admin_required
def users():
    """
    Displays the user management page for administrators.
    
    This route shows a list of all users in the system, allowing admins
    to view user information and manage user accounts. It requires admin
    privileges to access.
    
    Returns:
        str: Rendered user management template with user list
    """
    try:
        # Get all users for admin user management page
        all_users = User.query.all()
        
        # Convert users to serializable format for JavaScript
        users_data = []
        for user in all_users:
            users_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat() if user.created_at else None
            })
        
        # Render user management template
        return render_template('admin_functions/admin_manage_users.html', 
                               users=all_users, 
                               users_json=users_data)
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error in admin users route: {e}")
        
        # Return empty user list if database connection fails
        return render_template('admin_functions/admin_manage_users.html', 
                               users=[], 
                               users_json=[])

# Route: /admin/edit_user/<user_id> - Updates user account information
@admin_bp.route('/admin/edit_user/<int:user_id>', methods=['POST'])
@admin_required
def edit_user(user_id):
    """
    Handles user account updates by administrators.
    
    This route processes form submissions to update user information including
    username, email, and password. It validates that the new username doesn't
    conflict with existing users and updates the database accordingly.
    
    Args:
        user_id: ID of the user to be updated
    
    Returns:
        str: Redirect response to user management page
    """
    try:
        # Find user to edit
        user_to_edit = User.query.get(user_id)
        
        # Check if user exists
        if not user_to_edit:
            return redirect(url_for('admin.users'))
        
        # Get form data for user update
        new_username = request.form['username']
        new_email = request.form['email']
        new_password = request.form['password']
        
        # Check if new username already exists (excluding current user)
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user and existing_user.id != user_id:
            return redirect(url_for('admin.users'))
        
        # Update user in database
        user_to_edit.username = new_username
        user_to_edit.email = new_email
        if new_password:
            user_to_edit.set_password(new_password)
        save_database()
        
    except Exception as e:
        # Handle any errors during update
        print(f"Error in edit user route: {e}")
    
    # Redirect back to user management page
    return redirect(url_for('admin.users'))

# Route: /admin/delete_user/<user_id> - Deletes user account and all associated data
@admin_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    """
    Handles user account deletion by administrators.
    
    This route processes requests to delete user accounts and all associated
    data including categories and transactions. It provides confirmation
    feedback to the administrator.
    
    Args:
        user_id: ID of the user to be deleted
    
    Returns:
        str: Redirect response to user management page
    """
    try:
        # Get user to delete from database
        user_to_delete = User.query.get(user_id)
        
        # Check if user exists
        if not user_to_delete:
            return redirect(url_for('admin.users'))
        
        # Delete user and all associated data (cascade will handle categories and transactions)
        from app.models import db
        username = user_to_delete.username
        db.session.delete(user_to_delete)
        save_database()
        
    except Exception as e:
        # Handle any errors during deletion
        print(f"Error in delete user route: {e}")
    
    return redirect(url_for('admin.users'))

# Route: /admin/database - Shows raw database content for debugging
@admin_bp.route('/admin/database')
@admin_required
def view_database():
    """
    Displays the raw database content for administrators.
    
    This route provides a detailed view of all database content including
    users, categories, and transactions in both formatted and JSON formats.
    It's useful for debugging and system administration.
    
    Returns:
        str: Rendered database viewer template with all data
    """
    try:
        # Get database data for admin database viewer
        all_users = User.query.all()
        all_categories = Category.query.all()
        all_transactions = Transaction.query.all()
        
        # Convert data to JSON format for display
        users_json = json.dumps([user.to_dict() for user in all_users], indent=4)
        categories_json = json.dumps([category.to_dict() for category in all_categories], indent=4)
        transactions_json = json.dumps([transaction.to_dict() for transaction in all_transactions], indent=4)
        
        # Render database viewer template with all data
        return render_template('admin_functions/admin_view_database.html',
                               users_json=users_json,
                               categories_json=categories_json,
                               transactions_json=transactions_json,
                               users=all_users,
                               categories=all_categories,
                               transactions=all_transactions)
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error in admin database view route: {e}")
        
        # Return empty data if database connection fails
        return render_template('admin_functions/admin_view_database.html',
                               users_json='[]',
                               categories_json='[]',
                               transactions_json='[]',
                               users=[],
                               categories=[],
                               transactions=[]) 