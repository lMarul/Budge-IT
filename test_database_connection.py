#!/usr/bin/env python3
"""
Script to test database connection and diagnose sync issues
"""

import os
from sqlalchemy import text
from app import create_app, db
from app.models import User, Category, Transaction

def test_database_connection():
    """Test the current database connection"""
    print("🔍 Testing Database Connection")
    print("=" * 50)
    
    # Create app and get database URI
    app = create_app()
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    
    print(f"📊 Current Database URI: {db_uri}")
    print(f"🔧 Environment DATABASE_URL: {os.environ.get('DATABASE_URL', 'Not set')}")
    
    # Test database connection
    try:
        with app.app_context():
            # Test basic connection
            result = db.session.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            
            # Check if tables exist by trying to query them
            user_count = User.query.count()
            category_count = Category.query.count()
            transaction_count = Transaction.query.count()
            
            print(f"👥 Users: {user_count}")
            print(f"📂 Categories: {category_count}")
            print(f"💰 Transactions: {transaction_count}")
            
            # Show sample data
            if user_count > 0:
                users = User.query.limit(3).all()
                print(f"📝 Sample users: {[user.username for user in users]}")
            
            if transaction_count > 0:
                transactions = Transaction.query.limit(3).all()
                print(f"📝 Sample transactions: {[f'{t.item_name} - ${t.amount}' for t in transactions]}")
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    return True

def check_environment_setup():
    """Check environment variable setup"""
    print("\n🔧 Environment Setup Check")
    print("=" * 50)
    
    # Check for DATABASE_URL
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        print(f"✅ DATABASE_URL is set: {db_url[:50]}...")
    else:
        print("❌ DATABASE_URL is not set")
        print("💡 To use cloud database locally, set DATABASE_URL environment variable")
    
    # Check for SECRET_KEY
    secret_key = os.environ.get('SECRET_KEY')
    if secret_key:
        print("✅ SECRET_KEY is set")
    else:
        print("❌ SECRET_KEY is not set")
    
    # Check for FLASK_ENV
    flask_env = os.environ.get('FLASK_ENV')
    print(f"🌍 FLASK_ENV: {flask_env or 'Not set (defaults to development)'}")

def provide_solutions():
    """Provide solutions for common database sync issues"""
    print("\n💡 Solutions for Database Sync Issues")
    print("=" * 50)
    
    print("1. **For Local Development with Cloud Database:**")
    print("   Set environment variable:")
    print("   Windows: set DATABASE_URL=postgresql://user:pass@host:port/db")
    print("   Linux/Mac: export DATABASE_URL=postgresql://user:pass@host:port/db")
    
    print("\n2. **For Production Deployment:**")
    print("   - Vercel: Go to Project Settings → Environment Variables")
    print("   - Nhost: Set in nhost.env or dashboard")
    print("   - Add DATABASE_URL with your cloud database connection string")
    
    print("\n3. **Common Database URLs:**")
    print("   - Supabase: postgresql://postgres:[password]@[host]:5432/postgres")
    print("   - Nhost: postgresql://postgres:[password]@[host]:5432/postgres")
    print("   - Local SQLite: sqlite:///app.db")
    
    print("\n4. **To Force Cloud Database Locally:**")
    print("   Set DATABASE_URL before running the app")

if __name__ == "__main__":
    test_database_connection()
    check_environment_setup()
    provide_solutions() 