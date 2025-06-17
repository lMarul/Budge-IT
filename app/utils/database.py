# Vince - SQLAlchemy Database Utilities for Budget Tracker

import os
import json
from datetime import datetime
from flask import flash, current_app
import logging
import time
from sqlalchemy.exc import OperationalError, DisconnectionError, SQLAlchemyError, TimeoutError
from app.models import User, Category

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Database Connection Health Check ---

def check_database_connection():
    """
    Check if database connection is available with timeout.
    
    Returns:
        bool: True if connection is available, False otherwise
    """
    try:
        # Import db here to avoid circular imports
        from app import db
        from sqlalchemy import text
        # Try a simple query with timeout
        db.session.execute(text('SELECT 1'))
        db.session.commit()
        return True
    except (OperationalError, TimeoutError) as e:
        logger.warning(f"Database connection timeout/error: {e}")
        return False
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False

def retry_database_operation(operation, max_retries=3, delay=1):
    """
    Retry a database operation with exponential backoff.
    
    Args:
        operation: Function to retry
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
    
    Returns:
        Result of the operation or None if all retries failed
    """
    for attempt in range(max_retries):
        try:
            return operation()
        except (OperationalError, DisconnectionError) as e:
            if attempt == max_retries - 1:
                logger.error(f"Database operation failed after {max_retries} attempts: {e}")
                return None
            
            wait_time = delay * (2 ** attempt)  # Exponential backoff
            logger.warning(f"Database operation failed (attempt {attempt + 1}/{max_retries}), retrying in {wait_time}s: {e}")
            time.sleep(wait_time)
        except Exception as e:
            logger.error(f"Unexpected error in database operation: {e}")
            return None

# --- Jinja2 Custom Filters ---
def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    """Format datetime for display in templates."""
    if value is None:
        return ""
    return value.strftime(format)

def amount_color(amount):
    """Return CSS class for amount color based on value."""
    if amount is None:
        return ""
    return "text-success" if amount >= 0 else "text-danger"

# --- Database Helper Functions (SQLAlchemy) ---

def get_next_id(model_class):
    """
    Generates the next unique ID for a given model class.
    
    This function finds the highest existing ID in the specified model
    and returns the next available ID. It handles empty tables by
    starting with ID 1.
    
    Args:
        model_class: SQLAlchemy model class (User, Category, Transaction)
    
    Returns:
        int: Next available unique ID for the model
    """
    try:
        # Import db here to avoid circular imports
        from app import db
        # Get the maximum ID from the table
        max_id = db.session.query(db.func.max(model_class.id)).scalar()
        # Return maximum ID + 1, or 1 if table is empty
        return (max_id or 0) + 1
    except Exception as e:
        logger.error(f"Error getting next ID for {model_class.__name__}: {e}")
        return 1

def initialize_database(app):
    """
    Initialize the database on application startup.
    
    This function is called when the application starts to ensure
    the database is properly initialized and tables are created.
    """
    try:
        # Import db here to avoid circular imports
        from app import db
        # Initialize SQLAlchemy with the app
        db.init_app(app)
        
        with app.app_context():
            # Create all tables
            db.create_all()
            logger.info("Database tables created successfully!")
            
            # Check if we need to migrate from JSON
            json_file = app.config.get('DATABASE_FILE', 'budget_tracker.json')
            if os.path.exists(json_file):
                logger.info(f"Found existing JSON database: {json_file}")
                logger.info("You can run migration using migrate_from_json() function")
                
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        print(f"Database initialization error: {e}")

def save_database():
    """
    Save the current database state.
    
    This function commits any pending changes to the database.
    """
    try:
        # Import db here to avoid circular imports
        from app import db
        db.session.commit()
        logger.info("Database changes saved successfully!")
    except Exception as e:
        # Import db here to avoid circular imports
        from app import db
        db.session.rollback()
        logger.error(f"Error saving database: {e}")
        print(f"Error saving data: {e}")
        raise

# --- Model Helper Functions ---

def create_user(username, email, password):
    """
    Create a new user with error handling for Supabase connection limits.
    
    Args:
        username (str): Username for the new user
        email (str): Email address for the new user
        password (str): Password for the new user
        
    Returns:
        User: Created user object or None if creation failed
    """
    try:
        # Import db here to avoid circular imports
        from app import db
        
        # Check connection first
        if not check_database_connection():
            logger.error("Cannot create user - Supabase connection unavailable")
            return None
            
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            logger.warning(f"User creation failed - username {username} already exists")
            return None
            
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f"User {username} created successfully")
        return user
        
    except (OperationalError, TimeoutError) as e:
        logger.error(f"Supabase connection error during user creation: {e}")
        db.session.rollback()
        return None
    except SQLAlchemyError as e:
        logger.error(f"Database error during user creation: {e}")
        db.session.rollback()
        return None
    except Exception as e:
        logger.error(f"Unexpected error during user creation: {e}")
        db.session.rollback()
        return None

def create_preset_categories(user_id):
    """
    Create preset categories for a new user.
    
    Args:
        user_id: ID of the user to create categories for
    """
    try:
        # Preset income categories
        income_categories = [
            {'name': 'Salary', 'color': '#28a745'},
            {'name': 'Freelance', 'color': '#17a2b8'},
            {'name': 'Investment', 'color': '#ffc107'},
            {'name': 'Gift', 'color': '#e83e8c'},
            {'name': 'Other Income', 'color': '#6f42c1'}
        ]
        
        # Preset expense categories
        expense_categories = [
            {'name': 'Food & Dining', 'color': '#dc3545'},
            {'name': 'Transportation', 'color': '#fd7e14'},
            {'name': 'Shopping', 'color': '#6f42c1'},
            {'name': 'Bills & Utilities', 'color': '#20c997'},
            {'name': 'Entertainment', 'color': '#e83e8c'},
            {'name': 'Healthcare', 'color': '#28a745'},
            {'name': 'Education', 'color': '#17a2b8'},
            {'name': 'Housing', 'color': '#6c757d'},
            {'name': 'Other Expenses', 'color': '#495057'}
        ]
        
        # Create income categories
        for category_data in income_categories:
            category = Category(
                user_id=user_id,
                name=category_data['name'],
                category_type='income',
                color=category_data['color']
            )
            db.session.add(category)
        
        # Create expense categories
        for category_data in expense_categories:
            category = Category(
                user_id=user_id,
                name=category_data['name'],
                category_type='expense',
                color=category_data['color']
            )
            db.session.add(category)
        
        db.session.commit()
        logger.info(f"Created preset categories for user {user_id}")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating preset categories for user {user_id}: {e}")
        raise

def authenticate_user(username, password):
    """
    Authenticate user with improved error handling for Supabase connection limits.
    
    Args:
        username (str): Username to authenticate
        password (str): Password to verify
        
    Returns:
        User: Authenticated user object or None if authentication failed
    """
    try:
        # Import db here to avoid circular imports
        from app import db
        
        # Check connection first
        if not check_database_connection():
            logger.error("Cannot authenticate user - Supabase connection unavailable")
            return None
            
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            logger.info(f"User {username} authenticated successfully")
            return user
        else:
            logger.warning(f"Authentication failed for username: {username}")
            return None
            
    except (OperationalError, TimeoutError) as e:
        logger.error(f"Supabase connection error during authentication: {e}")
        return None
    except SQLAlchemyError as e:
        logger.error(f"Database error during authentication: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during authentication: {e}")
        return None

def get_user_by_id(user_id):
    """
    Get user by ID.
    
    Args:
        user_id: User ID to find
    
    Returns:
        User or None: User object if found, None otherwise
    """
    try:
        # Import models here to avoid circular imports
        from app.models import User
        return User.query.get(user_id)
    except Exception as e:
        logger.error(f"Error getting user by ID {user_id}: {e}")
        return None

def get_user_by_username(username):
    """
    Get user by username with error handling.
    
    Args:
        username (str): Username to search for
        
    Returns:
        User: User object or None if not found or error occurred
    """
    try:
        if not check_database_connection():
            logger.error("Cannot get user - Supabase connection unavailable")
            return None
            
        return User.query.filter_by(username=username).first()
        
    except (OperationalError, TimeoutError) as e:
        logger.error(f"Supabase connection error getting user: {e}")
        return None
    except Exception as e:
        logger.error(f"Error getting user {username}: {e}")
        return None

def create_category(name, user_id, category_type):
    """
    Create a new category with error handling.
    
    Args:
        name (str): Category name
        user_id (int): User ID who owns the category
        category_type (str): Type of category (income/expense)
        
    Returns:
        Category: Created category object or None if creation failed
    """
    try:
        # Import db here to avoid circular imports
        from app import db
        
        if not check_database_connection():
            logger.error("Cannot create category - Supabase connection unavailable")
            return None
            
        category = Category(name=name, user_id=user_id, type=category_type)
        db.session.add(category)
        db.session.commit()
        
        logger.info(f"Category {name} created successfully for user {user_id}")
        return category
        
    except (OperationalError, TimeoutError) as e:
        logger.error(f"Supabase connection error creating category: {e}")
        db.session.rollback()
        return None
    except SQLAlchemyError as e:
        logger.error(f"Database error creating category: {e}")
        db.session.rollback()
        return None
    except Exception as e:
        logger.error(f"Unexpected error creating category: {e}")
        db.session.rollback()
        return None

def get_categories_by_user_and_type(user_id, category_type):
    """
    Get categories for a user by type.
    
    Args:
        user_id: ID of the user
        category_type: Type of category ('income' or 'expense')
    
    Returns:
        list: List of Category objects
    """
    try:
        # Import models here to avoid circular imports
        from app.models import Category
        return Category.query.filter_by(
            user_id=user_id, 
            category_type=category_type
        ).all()
    except Exception as e:
        logger.error(f"Error getting categories for user {user_id}: {e}")
        return []

def create_transaction(user_id, amount, category_id, transaction_type, date, item_name):
    """
    Create a new transaction.
    
    Args:
        user_id: ID of the user who owns this transaction
        amount: Transaction amount
        category_id: ID of the category
        transaction_type: Type of transaction ('income' or 'expense')
        date: Transaction date
        item_name: Name/description of the transaction
    
    Returns:
        Transaction or None: New transaction object or None if creation failed
    """
    try:
        # Import models here to avoid circular imports
        from app.models import Transaction
        from app import db
        
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            category_id=category_id,
            transaction_type=transaction_type,
            date=date,
            item_name=item_name
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        logger.info(f"Transaction {item_name} created for user {user_id}")
        return transaction
        
    except Exception as e:
        # Import db here to avoid circular imports
        from app import db
        db.session.rollback()
        logger.error(f"Error creating transaction {item_name}: {e}")
        return None

def get_transactions_by_user(user_id):
    """
    Get all transactions for a user.
    
    Args:
        user_id: ID of the user
    
    Returns:
        list: List of Transaction objects
    """
    try:
        # Import models here to avoid circular imports
        from app.models import Transaction
        return Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc()).all()
    except Exception as e:
        logger.error(f"Error getting transactions for user {user_id}: {e}")
        return []

def get_transaction_by_id(transaction_id, user_id):
    """
    Get a specific transaction by ID, ensuring it belongs to the user.
    
    Args:
        transaction_id: ID of the transaction
        user_id: ID of the user (for security)
    
    Returns:
        Transaction or None: Transaction object if found and belongs to user, None otherwise
    """
    try:
        # Import models here to avoid circular imports
        from app.models import Transaction
        return Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    except Exception as e:
        logger.error(f"Error getting transaction {transaction_id} for user {user_id}: {e}")
        return None

def update_transaction(transaction_id, user_id, amount, item_name, date, category_id, transaction_type):
    """
    Update an existing transaction.
    
    Args:
        transaction_id: ID of the transaction to update
        user_id: ID of the user (for security)
        amount: New transaction amount
        item_name: New item name/description
        date: New transaction date
        category_id: New category ID
        transaction_type: New transaction type
    
    Returns:
        bool: True if update successful, False otherwise
    """
    try:
        # Import models here to avoid circular imports
        from app.models import Category
        from app import db
        
        transaction = get_transaction_by_id(transaction_id, user_id)
        if not transaction:
            logger.warning(f"Transaction {transaction_id} not found or unauthorized for user {user_id}")
            return False
        
        # Validate category belongs to user
        category = Category.query.filter_by(id=category_id, user_id=user_id).first()
        if not category:
            logger.warning(f"Category {category_id} not found or unauthorized for user {user_id}")
            return False
        
        # Update transaction fields
        transaction.amount = amount
        transaction.item_name = item_name
        transaction.date = date
        transaction.category_id = category_id
        transaction.transaction_type = transaction_type
        
        db.session.commit()
        logger.info(f"Transaction {transaction_id} updated successfully for user {user_id}")
        return True
        
    except Exception as e:
        # Import db here to avoid circular imports
        from app import db
        db.session.rollback()
        logger.error(f"Error updating transaction {transaction_id}: {e}")
        return False

def delete_transaction(transaction_id, user_id):
    """
    Delete a transaction.
    
    Args:
        transaction_id: ID of the transaction to delete
        user_id: ID of the user (for security)
    
    Returns:
        dict or None: Transaction data if deleted successfully, None otherwise
    """
    try:
        # Import db here to avoid circular imports
        from app import db
        
        transaction = get_transaction_by_id(transaction_id, user_id)
        if not transaction:
            logger.warning(f"Transaction {transaction_id} not found or unauthorized for user {user_id}")
            return None
        
        # Store transaction data for response
        transaction_data = {
            'id': transaction.id,
            'type': transaction.transaction_type,
            'amount': float(transaction.amount),
            'item_name': transaction.item_name
        }
        
        # Delete the transaction
        db.session.delete(transaction)
        db.session.commit()
        
        logger.info(f"Transaction {transaction_id} deleted successfully for user {user_id}")
        return transaction_data
        
    except Exception as e:
        # Import db here to avoid circular imports
        from app import db
        db.session.rollback()
        logger.error(f"Error deleting transaction {transaction_id}: {e}")
        return None

def migrate_from_json(json_file_path):
    """
    Migrate data from JSON file to SQLAlchemy database.
    
    This function reads the existing JSON database and creates corresponding
    records in the SQLAlchemy database.
    """
    # Import models here to avoid circular imports
    from app.models import migrate_from_json as model_migrate
    
    try:
        model_migrate(json_file_path)
        logger.info(f"Migration from {json_file_path} completed successfully")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise

def create_common_users():
    """
    Create common users for testing and recovery.
    
    This function creates a set of common users that might have existed
    in the previous database, allowing users to log in with familiar credentials.
    """
    try:
        # Import models here to avoid circular imports
        from app.models import User
        from app import db
        
        # List of common users to create
        common_users = [
            {'username': 'admin', 'email': 'admin@example.com', 'password': 'admin123'},
            {'username': 'user1', 'email': 'user1@example.com', 'password': 'password123'},
            {'username': 'test', 'email': 'test@example.com', 'password': 'test123'},
            {'username': 'demo', 'email': 'demo@example.com', 'password': 'demo123'},
            {'username': 'maru', 'email': 'maru@example.com', 'password': 'maru123'},
            {'username': 'anthony', 'email': 'anthony@example.com', 'password': 'anthony123'},
            {'username': 'vince', 'email': 'vince@example.com', 'password': 'vince123'},
            {'username': 'marwin', 'email': 'marwin@example.com', 'password': 'marwin123'},
        ]
        
        created_count = 0
        for user_data in common_users:
            # Check if user already exists
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if not existing_user:
                # Create new user
                user = User(username=user_data['username'], email=user_data['email'])
                user.set_password(user_data['password'])
                db.session.add(user)
                created_count += 1
                
                # Create preset categories for the new user
                create_preset_categories(user.id)
        
        db.session.commit()
        logger.info(f"Created {created_count} common users successfully")
        return created_count
        
    except Exception as e:
        # Import db here to avoid circular imports
        from app import db
        db.session.rollback()
        logger.error(f"Error creating common users: {e}")
        return 0

def get_all_users():
    """
    Get all users in the database.
    
    Returns:
        list: List of all User objects
    """
    try:
        # Import models here to avoid circular imports
        from app.models import User
        return User.query.all()
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        return []

def reset_user_password(username, new_password):
    """
    Reset a user's password.
    
    Args:
        username: Username of the user
        new_password: New password to set
    
    Returns:
        bool: True if password reset successful, False otherwise
    """
    try:
        # Import models here to avoid circular imports
        from app.models import User
        from app import db
        
        user = User.query.filter_by(username=username).first()
        if user:
            user.set_password(new_password)
            db.session.commit()
            logger.info(f"Password reset successful for user {username}")
            return True
        else:
            logger.warning(f"User {username} not found")
            return False
            
    except Exception as e:
        # Import db here to avoid circular imports
        from app import db
        db.session.rollback()
        logger.error(f"Error resetting password for user {username}: {e}")
        return False 