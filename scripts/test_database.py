#!/usr/bin/env python3
"""
Test script to verify SQLAlchemy setup and database connection.

This script tests the basic functionality of the SQLAlchemy models
and database connection without requiring Supabase.
"""

import os
import sys
from flask import Flask
from config import config
from models_sqlalchemy import db, User, Category, Transaction, init_db
from utils_sqlalchemy import create_user, authenticate_user, create_category, create_transaction

def test_sqlalchemy_setup():
    """Test the SQLAlchemy setup with SQLite database."""
    print("🧪 Testing SQLAlchemy Setup")
    print("=" * 40)
    
    # Create a test Flask app with SQLite database
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    try:
        # Initialize database
        print("🔧 Initializing database...")
        init_db(app)
        
        with app.app_context():
            # Test 1: Create a user
            print("\n📝 Test 1: Creating a test user...")
            test_user = create_user('testuser', 'test@example.com', 'password123')
            if test_user:
                print(f"✅ User created: {test_user.username} (ID: {test_user.id})")
            else:
                print("❌ Failed to create user")
                return False
            
            # Test 2: Authenticate user
            print("\n🔐 Test 2: Authenticating user...")
            auth_user = authenticate_user('testuser', 'password123')
            if auth_user:
                print(f"✅ User authenticated: {auth_user.username}")
            else:
                print("❌ Failed to authenticate user")
                return False
            
            # Test 3: Create a category
            print("\n📂 Test 3: Creating a test category...")
            test_category = create_category(test_user.id, 'Test Category', 'expense', '#FF0000')
            if test_category:
                print(f"✅ Category created: {test_category.name} (ID: {test_category.id})")
            else:
                print("❌ Failed to create category")
                return False
            
            # Test 4: Create a transaction
            print("\n💰 Test 4: Creating a test transaction...")
            from datetime import date
            test_transaction = create_transaction(
                test_user.id, 
                100.50, 
                test_category.id, 
                'expense', 
                date.today(), 
                'Test Transaction'
            )
            if test_transaction:
                print(f"✅ Transaction created: {test_transaction.item_name} (Amount: ${test_transaction.amount})")
            else:
                print("❌ Failed to create transaction")
                return False
            
            # Test 5: Query relationships
            print("\n🔗 Test 5: Testing relationships...")
            user_with_data = User.query.get(test_user.id)
            if user_with_data:
                print(f"✅ User has {len(user_with_data.categories)} categories")
                print(f"✅ User has {len(user_with_data.transactions)} transactions")
            else:
                print("❌ Failed to query user with relationships")
                return False
            
            # Test 6: Test data serialization
            print("\n📊 Test 6: Testing data serialization...")
            user_dict = test_user.to_dict()
            category_dict = test_category.to_dict()
            transaction_dict = test_transaction.to_dict()
            
            if all([user_dict, category_dict, transaction_dict]):
                print("✅ All models can be serialized to dictionaries")
            else:
                print("❌ Failed to serialize models")
                return False
            
            print("\n🎉 All tests passed! SQLAlchemy setup is working correctly.")
            print("\n📋 Summary:")
            print(f"   - Database: SQLite (test.db)")
            print(f"   - User: {test_user.username}")
            print(f"   - Category: {test_category.name}")
            print(f"   - Transaction: {test_transaction.item_name}")
            
            return True
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    
    finally:
        # Clean up test database
        try:
            if os.path.exists('test.db'):
                os.remove('test.db')
                print("\n🧹 Cleaned up test database")
        except:
            pass

def test_supabase_connection():
    """Test Supabase connection if DATABASE_URL is configured."""
    print("\n🌐 Testing Supabase Connection")
    print("=" * 40)
    
    # Check if DATABASE_URL is set
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("⚠️  No DATABASE_URL found in environment variables")
        print("   To test Supabase connection, set DATABASE_URL in your .env file")
        return False
    
    if not database_url.startswith('postgresql://'):
        print("⚠️  DATABASE_URL doesn't appear to be a PostgreSQL connection string")
        return False
    
    print(f"🔗 Found DATABASE_URL: {database_url[:50]}...")
    
    # Create a test Flask app with Supabase database
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    try:
        # Initialize database
        print("🔧 Initializing Supabase database...")
        init_db(app)
        
        with app.app_context():
            # Test connection by querying
            user_count = User.query.count()
            print(f"✅ Successfully connected to Supabase!")
            print(f"   Current users in database: {user_count}")
            return True
            
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        print("   Please check your DATABASE_URL and Supabase credentials")
        return False

if __name__ == "__main__":
    print("🚀 Budget Tracker - SQLAlchemy Setup Test")
    print("=" * 50)
    
    # Test with SQLite first
    sqlite_success = test_sqlalchemy_setup()
    
    # Test Supabase connection if available
    supabase_success = test_supabase_connection()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   SQLite Test: {'✅ PASSED' if sqlite_success else '❌ FAILED'}")
    print(f"   Supabase Test: {'✅ PASSED' if supabase_success else '⚠️  SKIPPED'}")
    
    if sqlite_success:
        print("\n🎉 SQLAlchemy setup is working correctly!")
        print("   You can now proceed with the migration to Supabase.")
    else:
        print("\n❌ SQLAlchemy setup has issues.")
        print("   Please check the error messages above.")
        sys.exit(1) 