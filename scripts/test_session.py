#!/usr/bin/env python3
"""
Test script to test session handling and authentication.
"""

import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, session
from config import config
from database.models import db, User, Category
from database.utils import get_categories_by_user_and_type

def create_app():
    """Create Flask app for database operations."""
    app = Flask(__name__)
    app.config.from_object(config['development'])
    db.init_app(app)
    return app

def test_session_simulation():
    """Test session simulation for get_categories route."""
    app = create_app()
    
    with app.app_context():
        try:
            # Get a non-admin user
            user = User.query.filter(User.username != 'admin').first()
            if not user:
                print("No non-admin users found")
                return
            
            print(f"Testing with user: {user.username} (ID: {user.id})")
            
            # Simulate session
            with app.test_request_context():
                session['user_id'] = user.id
                session['username'] = user.username
                
                print(f"Session user_id: {session.get('user_id')}")
                print(f"Session username: {session.get('username')}")
                
                # Test the get_categories logic with session
                user_id = session['user_id']
                income_categories = get_categories_by_user_and_type(user_id, 'income')
                expense_categories = get_categories_by_user_and_type(user_id, 'expense')
                
                print(f"Income categories: {len(income_categories)}")
                print(f"Expense categories: {len(expense_categories)}")
                
                # Convert categories to the format expected by the frontend
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
                
                print(f"Total categories data: {len(categories_data)}")
                print("Categories data:")
                for cat in categories_data:
                    print(f"  - {cat}")
            
        except Exception as e:
            print(f"Error: {e}")
            return 1
    
    return 0

if __name__ == '__main__':
    exit(test_session_simulation()) 