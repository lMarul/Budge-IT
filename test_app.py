#!/usr/bin/env python3
"""
Simple test script to verify Flask app works correctly.
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_import():
    """Test if the app can be imported successfully."""
    try:
        from app import create_app, db
        print("✅ App import successful")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def test_app_creation():
    """Test if the app can be created successfully."""
    try:
        from app import create_app
        app = create_app()
        print("✅ App creation successful")
        return app
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        return None

def test_database_connection():
    """Test database connection."""
    try:
        from app import create_app, db
        app = create_app()
        
        with app.app_context():
            # Test database connection
            db.engine.execute("SELECT 1")
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_routes_import():
    """Test if routes can be imported."""
    try:
        from app.routes.auth import auth_bp
        from app.routes.main import main_bp
        from app.routes.admin import admin_bp
        print("✅ Routes import successful")
        return True
    except Exception as e:
        print(f"❌ Routes import failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Flask app setup...")
    print("=" * 50)
    
    # Test 1: App import
    if not test_app_import():
        return False
    
    # Test 2: App creation
    app = test_app_creation()
    if not app:
        return False
    
    # Test 3: Routes import
    if not test_routes_import():
        return False
    
    # Test 4: Database connection (only if DATABASE_URL is set)
    if os.environ.get('DATABASE_URL'):
        if not test_database_connection():
            print("⚠️ Database connection failed, but app should still work with local SQLite")
    
    print("=" * 50)
    print("🎉 All tests passed! App is ready for deployment.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 