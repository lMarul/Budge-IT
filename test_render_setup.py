#!/usr/bin/env python3
"""
Test script to verify Render deployment setup
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import flask_sqlalchemy
        print("✅ Flask-SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"❌ Flask-SQLAlchemy import failed: {e}")
        return False
    
    try:
        import flask_login
        print("✅ Flask-Login imported successfully")
    except ImportError as e:
        print(f"❌ Flask-Login import failed: {e}")
        return False
    
    try:
        import psycopg2
        print("✅ psycopg2 imported successfully")
    except ImportError as e:
        print(f"❌ psycopg2 import failed: {e}")
        return False
    
    try:
        import gunicorn
        print("✅ gunicorn imported successfully")
    except ImportError as e:
        print(f"❌ gunicorn import failed: {e}")
        return False
    
    return True

def test_app_creation():
    """Test if the Flask app can be created"""
    print("\n🔍 Testing app creation...")
    
    try:
        from app import create_app
        app = create_app()
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        return False

def test_environment_variables():
    """Test environment variable setup"""
    print("\n🔍 Testing environment variables...")
    
    # Set test environment variables
    os.environ['FLASK_ENV'] = 'production'
    os.environ['SECRET_KEY'] = 'test-secret-key'
    
    if os.environ.get('DATABASE_URL'):
        print("✅ DATABASE_URL is set")
    else:
        print("⚠️ DATABASE_URL not set (this is normal for local testing)")
    
    print("✅ Environment variables configured")
    return True

def test_wsgi():
    """Test WSGI entry point"""
    print("\n🔍 Testing WSGI entry point...")
    
    try:
        from wsgi import app
        print("✅ WSGI app imported successfully")
        return True
    except Exception as e:
        print(f"❌ WSGI import failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Render Deployment Setup")
    print("=" * 40)
    
    # Run all tests
    tests = [
        test_imports,
        test_environment_variables,
        test_app_creation,
        test_wsgi
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your app is ready for Render deployment.")
        print("\n📋 Next steps:")
        print("1. Go to render.com and create a new Web Service")
        print("2. Connect your GitHub repository")
        print("3. Set environment variables:")
        print("   - DATABASE_URL (your Supabase connection string)")
        print("   - SECRET_KEY (your secret key)")
        print("   - FLASK_ENV=production")
        print("4. Deploy!")
    else:
        print("❌ Some tests failed. Please fix the issues before deploying.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 