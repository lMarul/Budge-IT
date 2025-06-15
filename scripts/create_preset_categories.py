#!/usr/bin/env python3
"""
Script to create preset categories for existing users who don't have any categories.

This script checks all users in the database and creates preset categories
for those who don't have any categories yet.
"""

import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from config import config
from database.models import db, User, Category
from database.utils import create_preset_categories

def create_app():
    """Create Flask app for database operations."""
    app = Flask(__name__)
    app.config.from_object(config['development'])
    db.init_app(app)
    return app

def main():
    """Main function to create preset categories for users without categories."""
    app = create_app()
    
    with app.app_context():
        try:
            # Get all users
            users = User.query.all()
            print(f"Found {len(users)} users in the database")
            
            users_without_categories = []
            
            for user in users:
                # Check if user has any categories
                categories = Category.query.filter_by(user_id=user.id).all()
                
                if not categories:
                    users_without_categories.append(user)
                    print(f"User '{user.username}' has no categories")
            
            if not users_without_categories:
                print("All users already have categories. No action needed.")
                return
            
            print(f"\nFound {len(users_without_categories)} users without categories:")
            for user in users_without_categories:
                print(f"- {user.username}")
            
            # Ask for confirmation
            response = input(f"\nDo you want to create preset categories for these users? (y/N): ")
            if response.lower() != 'y':
                print("Operation cancelled.")
                return
            
            # Create preset categories for each user
            for user in users_without_categories:
                try:
                    create_preset_categories(user.id)
                    print(f"✓ Created preset categories for user '{user.username}'")
                except Exception as e:
                    print(f"✗ Error creating categories for user '{user.username}': {e}")
            
            print("\nPreset categories creation completed!")
            
        except Exception as e:
            print(f"Error: {e}")
            return 1
    
    return 0

if __name__ == '__main__':
    exit(main()) 