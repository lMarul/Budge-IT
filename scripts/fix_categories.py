#!/usr/bin/env python3
"""
Script to automatically create preset categories for users who don't have any categories.
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
            # Get all users except admin
            users = User.query.filter(User.username != 'admin').all()
            print(f"Found {len(users)} non-admin users in the database")
            
            users_without_categories = []
            
            for user in users:
                # Check if user has any categories
                categories = Category.query.filter_by(user_id=user.id).all()
                
                if not categories:
                    users_without_categories.append(user)
                    print(f"User '{user.username}' has no categories")
            
            if not users_without_categories:
                print("All non-admin users already have categories. No action needed.")
                return 0
            
            print(f"\nCreating preset categories for {len(users_without_categories)} users:")
            for user in users_without_categories:
                print(f"- {user.username}")
            
            # Create preset categories for each user
            for user in users_without_categories:
                try:
                    create_preset_categories(user.id)
                    print(f"✓ Created preset categories for user '{user.username}'")
                except Exception as e:
                    print(f"✗ Error creating categories for user '{user.username}': {e}")
            
            print("\nPreset categories creation completed!")
            return 0
            
        except Exception as e:
            print(f"Error: {e}")
            return 1
    
    return 0

if __name__ == '__main__':
    exit(main()) 