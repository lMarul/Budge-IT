#!/usr/bin/env python3
"""
Test script to check the current state of categories in the database.
"""

import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from config import config
from database.models import db, User, Category

def create_app():
    """Create Flask app for database operations."""
    app = Flask(__name__)
    app.config.from_object(config['development'])
    db.init_app(app)
    return app

def main():
    """Main function to test categories."""
    app = create_app()
    
    with app.app_context():
        try:
            # Get all users
            users = User.query.all()
            print(f"Found {len(users)} users in the database:")
            
            for user in users:
                print(f"\nUser: {user.username} (ID: {user.id})")
                
                # Check categories for this user
                categories = Category.query.filter_by(user_id=user.id).all()
                print(f"  Categories: {len(categories)}")
                
                for category in categories:
                    print(f"    - {category.name} ({category.category_type}) - Color: {category.color}")
                
                if not categories:
                    print("    No categories found")
            
            # Test the get_categories route logic
            print(f"\n--- Testing get_categories logic ---")
            for user in users:
                if user.username != 'admin':  # Skip admin
                    print(f"\nFor user '{user.username}':")
                    income_categories = Category.query.filter_by(user_id=user.id, category_type='income').all()
                    expense_categories = Category.query.filter_by(user_id=user.id, category_type='expense').all()
                    
                    print(f"  Income categories: {len(income_categories)}")
                    print(f"  Expense categories: {len(expense_categories)}")
                    
                    # Test the format that would be returned by get_categories
                    categories_data = []
                    
                    for category in income_categories:
                        categories_data.append({
                            'id': category.id,
                            'name': category.name,
                            'type': category.category_type,
                            'color': category.color
                        })
                    
                    for category in expense_categories:
                        categories_data.append({
                            'id': category.id,
                            'name': category.name,
                            'type': category.category_type,
                            'color': category.color
                        })
                    
                    print(f"  Total categories data: {len(categories_data)}")
                    if categories_data:
                        print(f"  Sample data: {categories_data[0] if categories_data else 'None'}")
            
        except Exception as e:
            print(f"Error: {e}")
            return 1
    
    return 0

if __name__ == '__main__':
    exit(main()) 