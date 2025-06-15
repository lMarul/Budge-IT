#!/usr/bin/env python3
"""
Script to add preset categories for admin user.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from database.utils import create_preset_categories
from database.models import User

def add_admin_categories():
    """Add preset categories for admin user."""
    with app.app_context():
        print("Adding preset categories for admin user...")
        
        # Get admin user
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Admin user not found. Please create an admin user first.")
            return False
        
        user_id = user.id
        print(f"✅ Found user: {user.username} (ID: {user_id})")
        
        # Add preset categories
        try:
            create_preset_categories(user_id)
            print("✅ Preset categories created successfully!")
            return True
        except Exception as e:
            print(f"❌ Error creating preset categories: {e}")
            return False

if __name__ == "__main__":
    success = add_admin_categories()
    if success:
        print("\n🎉 Admin categories added successfully!")
        print("You can now add test transactions.")
    else:
        print("\n💥 Failed to add admin categories!") 