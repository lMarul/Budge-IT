#!/usr/bin/env python3
"""
Test script to test API endpoints directly.
"""

import sys
import os
import requests
import json

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from config import config
from database.models import db, User, Category
from database.utils import get_categories_by_user_and_type

def create_app():
    """Create Flask app for database operations."""
    app = Flask(__name__)
    app.config.from_object(config['development'])
    db.init_app(app)
    return app

def test_get_categories_logic():
    """Test the get_categories route logic directly."""
    app = create_app()
    
    with app.app_context():
        try:
            # Get a non-admin user
            user = User.query.filter(User.username != 'admin').first()
            if not user:
                print("No non-admin users found")
                return
            
            print(f"Testing with user: {user.username} (ID: {user.id})")
            
            # Test the get_categories logic
            income_categories = get_categories_by_user_and_type(user.id, 'income')
            expense_categories = get_categories_by_user_and_type(user.id, 'expense')
            
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
            
            # Test filtering
            income_only = [cat for cat in categories_data if cat['type'] == 'income']
            expense_only = [cat for cat in categories_data if cat['type'] == 'expense']
            
            print(f"\nFiltered income categories: {len(income_only)}")
            for cat in income_only:
                print(f"  - {cat['name']}")
            
            print(f"\nFiltered expense categories: {len(expense_only)}")
            for cat in expense_only:
                print(f"  - {cat['name']}")
            
        except Exception as e:
            print(f"Error: {e}")
            return 1
    
    return 0

if __name__ == '__main__':
    exit(test_get_categories_logic()) 