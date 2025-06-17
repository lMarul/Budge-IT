#!/usr/bin/env python3
"""
Quick Test Script for Budget Tracker
====================================

This script provides a quick way to test the application during development.
It runs essential tests and provides immediate feedback.

Usage:
    python quick_test.py
"""

import sys
import os
from datetime import datetime

def run_quick_tests():
    """Run quick essential tests"""
    print("🚀 Running Quick Tests...")
    print("=" * 40)
    
    try:
        # Test 1: Import application
        print("1. Testing application imports...")
        from app import create_app, db
        from app.models import User, Category, Transaction
        print("   ✅ All imports successful")
        
        # Test 2: Create test app
        print("2. Testing app creation...")
        from test_config import TestConfig
        app = create_app()
        app.config.from_object(TestConfig)
        print("   ✅ Test app created successfully")
        
        # Test 3: Database setup
        print("3. Testing database setup...")
        with app.app_context():
            db.create_all()
            print("   ✅ Database tables created")
        
        # Test 4: Test client
        print("4. Testing client creation...")
        client = app.test_client()
        print("   ✅ Test client created")
        
        # Test 5: Basic routes
        print("5. Testing basic routes...")
        
        # Health check
        response = client.get('/health')
        if response.status_code == 200:
            print("   ✅ Health check endpoint working")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
        
        # Root route
        response = client.get('/')
        if response.status_code in [200, 302]:
            print("   ✅ Root route accessible")
        else:
            print(f"   ❌ Root route failed: {response.status_code}")
            return False
        
        # Test 6: Database connection
        print("6. Testing database connection...")
        response = client.get('/test-db')
        if response.status_code == 200:
            print("   ✅ Database connection successful")
        else:
            print(f"   ❌ Database connection failed: {response.status_code}")
            return False
        
        print("\n" + "=" * 40)
        print("✅ ALL QUICK TESTS PASSED!")
        print("The application is ready for development.")
        print("=" * 40)
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        print("   Make sure all dependencies are installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

def check_environment():
    """Check if the environment is properly set up"""
    print("🔍 Checking environment...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 8:
        print(f"   ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"   ⚠️  Python {python_version.major}.{python_version.minor}.{python_version.micro} (3.8+ recommended)")
    
    # Check if we're in the right directory
    if os.path.exists('app') and os.path.exists('requirements.txt'):
        print("   ✅ Project structure looks good")
    else:
        print("   ❌ Not in the correct project directory")
        return False
    
    # Check for key files
    required_files = ['app/__init__.py', 'app/models/__init__.py', 'wsgi.py']
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file} exists")
        else:
            print(f"   ❌ {file} missing")
            return False
    
    return True

def main():
    """Main function"""
    print("🧪 BUDGET TRACKER - QUICK TEST")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Check environment first
    if not check_environment():
        print("\n❌ Environment check failed. Please fix the issues above.")
        return 1
    
    print()
    
    # Run quick tests
    success = run_quick_tests()
    
    if success:
        print("\n🎉 Ready to proceed with development!")
        print("\nNext steps:")
        print("1. Run full test suite: python run_tests.py")
        print("2. Start development server: python wsgi.py")
        print("3. View testing documentation: cat TESTING.md")
        return 0
    else:
        print("\n❌ Quick tests failed. Please check the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 