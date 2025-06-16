#!/usr/bin/env python3
"""
Vercel Deployment Helper Script
This script helps prepare and test your Flask app for Vercel deployment.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_requirements():
    """Check if all required files exist."""
    required_files = [
        'wsgi.py',
        'requirements.txt',
        'vercel.json',
        'app/__init__.py',
        'app/models/__init__.py',
        'app/routes/auth.py',
        'app/routes/main.py',
        'app/routes/admin.py',
        'app/utils/database.py',
        'app/decorators.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    else:
        print("✅ All required files found")
        return True

def check_imports():
    """Test if all imports work correctly."""
    try:
        # Test basic app import
        from app import create_app, db
        print("✅ App imports successful")
        
        # Test route imports
        from app.routes.auth import auth_bp
        from app.routes.main import main_bp
        from app.routes.admin import admin_bp
        print("✅ Route imports successful")
        
        # Test model imports
        from app.models import User, Category, Transaction
        print("✅ Model imports successful")
        
        # Test utility imports
        from app.utils.database import create_user, authenticate_user
        print("✅ Utility imports successful")
        
        # Test decorator imports
        from app.decorators import login_required, admin_required
        print("✅ Decorator imports successful")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def check_vercel_config():
    """Check Vercel configuration."""
    try:
        with open('vercel.json', 'r') as f:
            config = json.load(f)
        
        required_keys = ['version', 'builds', 'routes']
        for key in required_keys:
            if key not in config:
                print(f"❌ Missing '{key}' in vercel.json")
                return False
        
        print("✅ Vercel configuration valid")
        return True
    except Exception as e:
        print(f"❌ Vercel config error: {e}")
        return False

def check_requirements_txt():
    """Check requirements.txt file."""
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        
        required_packages = [
            'Flask',
            'Flask-SQLAlchemy',
            'Flask-Login',
            'psycopg2-binary',
            'python-dotenv'
        ]
        
        missing_packages = []
        for package in required_packages:
            if package not in requirements:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Missing packages in requirements.txt: {missing_packages}")
            return False
        else:
            print("✅ All required packages in requirements.txt")
            return True
    except Exception as e:
        print(f"❌ Requirements.txt error: {e}")
        return False

def test_app_creation():
    """Test if the app can be created successfully."""
    try:
        from app import create_app
        app = create_app()
        print("✅ App creation successful")
        return True
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        return False

def check_environment_variables():
    """Check if required environment variables are documented."""
    env_template = Path('env_template.txt')
    if env_template.exists():
        print("✅ Environment template found")
        return True
    else:
        print("⚠️ Environment template not found (optional)")
        return True

def generate_deployment_summary():
    """Generate a deployment summary."""
    print("\n" + "="*60)
    print("🚀 VERCEL DEPLOYMENT SUMMARY")
    print("="*60)
    
    print("\n📋 Required Environment Variables:")
    print("DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres")
    print("SECRET_KEY=your-super-secret-key-here")
    print("FLASK_ENV=production")
    
    print("\n🔧 Deployment Steps:")
    print("1. Push code to Git repository")
    print("2. Connect repository to Vercel")
    print("3. Set environment variables in Vercel dashboard")
    print("4. Deploy and test")
    
    print("\n📁 Key Files:")
    print("- wsgi.py (entry point)")
    print("- vercel.json (configuration)")
    print("- requirements.txt (dependencies)")
    print("- app/ (Flask application)")
    
    print("\n🔗 Useful Links:")
    print("- Vercel Dashboard: https://vercel.com/dashboard")
    print("- Supabase Dashboard: https://supabase.com/dashboard")
    print("- Deployment Guide: VERCEL_DEPLOYMENT.md")

def main():
    """Run all deployment checks."""
    print("🔍 Vercel Deployment Pre-Check")
    print("="*40)
    
    checks = [
        ("File Structure", check_requirements),
        ("Import Statements", check_imports),
        ("Vercel Configuration", check_vercel_config),
        ("Requirements File", check_requirements_txt),
        ("App Creation", test_app_creation),
        ("Environment Variables", check_environment_variables)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n🔍 {check_name}...")
        if not check_func():
            all_passed = False
    
    if all_passed:
        print("\n🎉 All checks passed! Your app is ready for Vercel deployment.")
        generate_deployment_summary()
    else:
        print("\n❌ Some checks failed. Please fix the issues before deploying.")
        print("Check the error messages above and refer to VERCEL_DEPLOYMENT.md for help.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 