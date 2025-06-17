# Vince - SQLAlchemy Database Utilities for Budget Tracker

import os
import json
from datetime import datetime
from flask import flash
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Jinja2 Custom Filters ---
def datetimeformat(value, format='%B %d, %Y'):
    """
    Custom Jinja2 filter for formatting datetime strings in templates.
    
    This function takes a datetime string and formats it according to the specified
    format string. It handles invalid or missing dates gracefully by returning 'N/A'.
    
    Args:
        value: ISO-formatted datetime string or None
        format: Format string for datetime output (default: '%B %d, %Y')
    
    Returns:
        str: Formatted date string or 'N/A' if invalid/missing
    """
    # Return N/A if value is empty or already N/A
    if not value or value == 'N/A':
        return "N/A"
    
    try:
        # Convert ISO string to datetime object for formatting
        dt_object = datetime.fromisoformat(value)
        # Return formatted date string
        return dt_object.strftime(format)
    except (ValueError, TypeError):
        # Return N/A for invalid date formats
        return "N/A"

def amount_color(value):
    """
    Custom Jinja2 filter for determining color class based on amount value.
    
    This function takes a numeric value and returns the appropriate CSS color class:
    - Gray for zero values
    - Green for positive values  
    - Red for negative values
    
    Args:
        value: Numeric value (int, float, or string that can be converted to float)
    
    Returns:
        str: CSS color class string for Tailwind CSS
    """
    try:
        # Convert to float and handle edge cases
        if value is None:
            return "text-gray-500 dark:text-gray-400"
        
        # Convert to float, handling string inputs
        num_value = float(value)
        
        # Handle edge cases
        if num_value == 0:
            return "text-gray-500 dark:text-gray-400"
        elif num_value > 0:
            return "text-green-600 dark:text-green-400"
        else:  # num_value < 0
            return "text-red-600 dark:text-red-400"
            
    except (ValueError, TypeError):
        # Return gray for invalid values
        return "text-gray-500 dark:text-gray-400"

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
    Create a new user in the database.
    
    Args:
        username: Unique username for the new account
        email: Email address for the new account
        password: Plain text password (will be hashed)
    
    Returns:
        User: New user object or None if creation failed
    """
    try:
        # Import models and db here to avoid circular imports
        from app.models import User
        from app import db
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            logger.warning(f"User {username} already exists")
            return None
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Create preset categories for the new user
        create_preset_categories(user.id)
        
        logger.info(f"User {username} created successfully with preset categories")
        return user
        
    except Exception as e:
        # Import db here to avoid circular imports
        from app import db
        db.session.rollback()
        logger.error(f"Error creating user {username}: {e}")
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
    Authenticate a user login attempt.
    
    Args:
        username: Username to authenticate
        password: Plain text password to verify
    
    Returns:
        User or None: User object if authentication successful, None otherwise
    """
    try:
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            logger.info(f"User {username} authenticated successfully")
            return user
        logger.warning(f"Authentication failed for user {username}")
        return None
    except Exception as e:
        logger.error(f"Error authenticating user {username}: {e}")
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
        return User.query.get(user_id)
    except Exception as e:
        logger.error(f"Error getting user by ID {user_id}: {e}")
        return None

def get_user_by_username(username):
    """
    Get user by username.
    
    Args:
        username: Username to find
    
    Returns:
        User or None: User object if found, None otherwise
    """
    try:
        return User.query.filter_by(username=username).first()
    except Exception as e:
        logger.error(f"Error getting user by username {username}: {e}")
        return None

def create_category(user_id, name, category_type, color):
    """
    Create a new category for a user.
    
    Args:
        user_id: ID of the user who owns this category
        name: Name of the category
        category_type: Type of category ('income' or 'expense')
        color: Hex color code for category display
    
    Returns:
        Category or None: New category object or None if creation failed
    """
    try:
        category = Category(
            user_id=user_id,
            name=name,
            category_type=category_type,
            color=color
        )
        
        db.session.add(category)
        db.session.commit()
        
        logger.info(f"Category {name} created for user {user_id}")
        return category
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating category {name}: {e}")
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
        db.session.rollback()
        logger.error(f"Error deleting transaction {transaction_id}: {e}")
        return None

def migrate_from_json(json_file_path):
    """
    Migrate data from JSON file to SQLAlchemy database.
    
    This function reads the existing JSON database and creates corresponding
    records in the SQLAlchemy database.
    """
    from models_sqlalchemy import migrate_from_json as model_migrate
    
    try:
        model_migrate(json_file_path)
        logger.info(f"Migration from {json_file_path} completed successfully")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise 