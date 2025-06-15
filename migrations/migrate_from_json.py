#!/usr/bin/env python3
"""
Migration script to convert from JSON database to SQLAlchemy database.

This script helps migrate existing data from the JSON-based database
to the new SQLAlchemy database system for Supabase integration.

Usage:
    python migrate_to_sqlalchemy.py
"""

import os
import sys
from flask import Flask
from config import config
from models_sqlalchemy import db, init_db, migrate_from_json

def create_migration_app():
    """Create a Flask app for migration purposes."""
    app = Flask(__name__)
    
    # Use development configuration for migration
    app.config.from_object(config['development'])
    
    return app

def main():
    """Main migration function."""
    print("=== Budget Tracker Database Migration ===")
    print("This script will migrate your data from JSON to SQLAlchemy database.")
    print()
    
    # Check if JSON database exists
    json_file = 'budget_tracker.json'
    if not os.path.exists(json_file):
        print(f"❌ JSON database file '{json_file}' not found.")
        print("No migration needed or file is missing.")
        return
    
    # Create Flask app
    app = create_migration_app()
    
    try:
        # Initialize database
        print("🔧 Initializing SQLAlchemy database...")
        init_db(app)
        
        with app.app_context():
            # Check if database is empty
            from models_sqlalchemy import User
            user_count = User.query.count()
            
            if user_count > 0:
                print(f"⚠️  Database already contains {user_count} users.")
                response = input("Do you want to continue with migration? (y/N): ")
                if response.lower() != 'y':
                    print("Migration cancelled.")
                    return
            
            # Perform migration
            print("🔄 Starting data migration...")
            migrate_from_json(json_file)
            
            # Verify migration
            print("✅ Migration completed!")
            print()
            
            # Show migration results
            user_count = User.query.count()
            from models_sqlalchemy import Category, Transaction
            category_count = Category.query.count()
            transaction_count = Transaction.query.count()
            
            print("📊 Migration Results:")
            print(f"   Users migrated: {user_count}")
            print(f"   Categories migrated: {category_count}")
            print(f"   Transactions migrated: {transaction_count}")
            print()
            
            # Backup original JSON file
            backup_file = f"{json_file}.backup"
            if not os.path.exists(backup_file):
                import shutil
                shutil.copy2(json_file, backup_file)
                print(f"💾 Original JSON file backed up as '{backup_file}'")
            
            print("🎉 Migration successful!")
            print()
            print("Next steps:")
            print("1. Update your app.py to use the new SQLAlchemy models")
            print("2. Set up your Supabase database connection")
            print("3. Test your application with the new database")
            print("4. Remove the old JSON file once you're satisfied")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print("Please check your database configuration and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main() 